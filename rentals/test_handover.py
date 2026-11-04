from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from threading import Barrier

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, close_old_connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from .models import RentalItem, Reservation
from .services import cancel_reservation, issue_reservation, reserve_item, return_reservation
from .test_reservations import create_equipment


def create_booking(item, user):
    today = timezone.localdate()
    return reserve_item(user=user, item_id=item.pk, start_date=today, end_date=today+timedelta(days=2), quoted_rate=Decimal("25.50"))


class HandoverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.customer = get_user_model().objects.create_user(username="handover-client")
        cls.staff = get_user_model().objects.create_user(username="handover-admin", is_staff=True, is_superuser=True)
        cls.item = create_equipment()

    def setUp(self):
        self.booking = create_booking(self.item, self.customer)

    def issue(self):
        return issue_reservation(reservation_id=self.booking.pk, user=self.staff)

    def test_issue_and_return_record_employee_and_release_item_without_changing_price_or_sale_stock(self):
        booking = self.issue()
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "rented")
        self.assertEqual(booking.status, "issued")
        self.assertEqual(booking.issued_by, self.staff)
        self.assertIsNotNone(booking.issued_at)
        returned = return_reservation(reservation_id=booking.pk, user=self.staff)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "available")
        self.assertEqual(returned.status, "returned")
        self.assertEqual(returned.returned_by, self.staff)
        self.assertGreaterEqual(returned.returned_at, returned.issued_at)
        self.assertEqual(returned.total_price, Decimal("76.50"))
        self.item.product.refresh_from_db()
        self.assertEqual(self.item.product.sale_stock, 7)
        self.assertEqual(create_booking(self.item, self.customer).status, "confirmed")

    def test_return_to_service_blocks_new_reservations(self):
        self.issue()
        returned = return_reservation(reservation_id=self.booking.pk, user=self.staff, to_service=True)
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "service")
        self.assertTrue(returned.returned_to_service)
        with self.assertRaises(ValidationError):
            create_booking(self.item, self.customer)

    def test_repeating_issue_and_return_preserves_original_timestamps_and_outcome(self):
        issued = self.issue()
        self.assertEqual(self.issue().issued_at, issued.issued_at)
        returned = return_reservation(reservation_id=self.booking.pk, user=self.staff)
        self.assertEqual(return_reservation(reservation_id=self.booking.pk, user=self.staff).returned_at, returned.returned_at)
        with self.assertRaises(ValidationError):
            return_reservation(reservation_id=self.booking.pk, user=self.staff, to_service=True)

    def test_customer_and_staff_without_both_permissions_cannot_operate(self):
        limited = get_user_model().objects.create_user(username="handover-limited", is_staff=True)
        limited.user_permissions.add(Permission.objects.get(codename="change_reservation"))
        for user in (self.customer, limited):
            for operation in (issue_reservation, return_reservation):
                with self.subTest(user=user.username, operation=operation.__name__):
                    with self.assertRaises(PermissionDenied):
                        operation(reservation_id=self.booking.pk, user=user)
        limited.user_permissions.add(Permission.objects.get(codename="change_rentalitem"))
        limited = get_user_model().objects.get(pk=limited.pk)
        self.assertEqual(issue_reservation(reservation_id=self.booking.pk, user=limited).status, "issued")

    def test_issue_rejects_future_expired_cancelled_and_returned_reservations(self):
        today = timezone.localdate()
        for start, end in ((today+timedelta(days=1), today+timedelta(days=2)), (today-timedelta(days=2), today-timedelta(days=1))):
            Reservation.objects.filter(pk=self.booking.pk).update(start_date=start, end_date=end)
            with self.assertRaises(ValidationError):
                self.issue()
        Reservation.objects.filter(pk=self.booking.pk).update(start_date=today, end_date=today)
        cancel_reservation(reservation_id=self.booking.pk, user=self.customer)
        with self.assertRaises(ValidationError):
            self.issue()
        self.booking = create_booking(self.item, self.customer)
        self.issue()
        return_reservation(reservation_id=self.booking.pk, user=self.staff)
        with self.assertRaises(ValidationError):
            self.issue()

    def test_service_or_hidden_item_cannot_be_issued(self):
        for changes in ({"status": "service"}, {"is_active": False}):
            RentalItem.objects.filter(pk=self.item.pk).update(status="available", is_active=True)
            RentalItem.objects.filter(pk=self.item.pk).update(**changes)
            with self.assertRaises(ValidationError):
                self.issue()
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")
        self.assertIsNone(self.booking.issued_at)

    def test_cannot_return_before_issue_or_cancel_after_issue_or_return(self):
        with self.assertRaises(ValidationError):
            return_reservation(reservation_id=self.booking.pk, user=self.staff)
        self.issue()
        with self.assertRaises(ValidationError):
            cancel_reservation(reservation_id=self.booking.pk, user=self.customer)
        return_reservation(reservation_id=self.booking.pk, user=self.staff)
        with self.assertRaises(ValidationError):
            cancel_reservation(reservation_id=self.booking.pk, user=self.staff, as_staff=True)

    def test_overdue_unreturned_item_blocks_all_future_dates_even_if_item_status_is_changed(self):
        self.issue()
        today = timezone.localdate()
        Reservation.objects.filter(pk=self.booking.pk).update(start_date=today-timedelta(days=3), end_date=today-timedelta(days=1))
        RentalItem.objects.filter(pk=self.item.pk).update(status="available")
        future = today+timedelta(days=30)
        with self.assertRaises(ValidationError):
            reserve_item(user=self.customer, item_id=self.item.pk, start_date=future, end_date=future, quoted_rate=Decimal("25.50"))
        response = self.client.get(reverse("rentals:list"), {"start_date": future.isoformat(), "end_date": future.isoformat()})
        self.assertEqual(response.context["items"], [])
        self.assertFalse(self.client.get(reverse("rentals:detail", args=[self.item.pk])).context["available"])
        self.client.force_login(self.customer)
        self.assertContains(self.client.get(reverse("rentals:mine")), "Termin zwrotu minął")

    def test_database_rejects_inconsistent_events_and_two_active_issues(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Reservation.objects.filter(pk=self.booking.pk).update(status="issued")
        issued = self.issue()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Reservation.objects.create(user=self.customer, item=self.item, start_date=issued.start_date, end_date=issued.end_date, daily_rate=issued.daily_rate, product_name="Copy", size="M", status="issued", issued_at=issued.issued_at, issued_by=self.staff)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Reservation.objects.filter(pk=issued.pk).update(status="returned", returned_at=issued.issued_at-timedelta(seconds=1), returned_by=self.staff)

    def test_admin_actions_operate_and_item_status_is_readonly_while_issued(self):
        self.client.force_login(self.staff)
        url = reverse("admin:rentals_reservation_changelist")
        for action, expected in (("issue_selected", "issued"), ("return_to_service_selected", "returned")):
            response = self.client.post(url, {"action": action, "_selected_action": [self.booking.pk]})
            self.assertEqual(response.status_code, 302)
            self.booking.refresh_from_db()
            self.assertEqual(self.booking.status, expected)
            if expected == "issued":
                response = self.client.get(reverse("admin:rentals_rentalitem_change", args=[self.item.pk]))
                self.assertNotContains(response, 'name="status"')
        self.item.refresh_from_db()
        self.assertEqual(self.item.status, "service")

    def test_admin_actions_require_csrf_and_are_hidden_without_item_permission(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.staff)
        url = reverse("admin:rentals_reservation_changelist")
        self.assertEqual(client.post(url, {"action": "issue_selected", "_selected_action": [self.booking.pk]}).status_code, 403)
        limited = get_user_model().objects.create_user(username="view-handover", is_staff=True)
        limited.user_permissions.add(Permission.objects.get(codename="change_reservation"))
        self.client.force_login(limited)
        self.assertNotContains(self.client.get(url), 'value="issue_selected"')
        self.client.post(url, {"action": "issue_selected", "_selected_action": [self.booking.pk]})
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")

    def test_english_customer_history_shows_actual_issue_and_return(self):
        self.issue()
        self.client.force_login(self.customer)
        self.client.cookies["django_language"] = "en"
        response = self.client.get(reverse("rentals:mine"))
        self.assertContains(response, "Rented out")
        self.assertContains(response, "Issued")
        self.assertNotContains(response, 'action="'+reverse("rentals:cancel", args=[self.booking.pk])+'"')
        return_reservation(reservation_id=self.booking.pk, user=self.staff)
        self.assertContains(self.client.get(reverse("rentals:mine")), "Returned")


class ConcurrentHandoverTests(TransactionTestCase):
    def test_repeated_simultaneous_issue_creates_one_event(self):
        item = create_equipment()
        user = get_user_model().objects.create_user(username="thread-client")
        staff = get_user_model().objects.create_user(username="thread-staff", is_staff=True, is_superuser=True)
        booking = create_booking(item, user)
        barrier = Barrier(2)
        def attempt(_):
            close_old_connections()
            try:
                actor = get_user_model().objects.get(pk=staff.pk)
                barrier.wait(timeout=10)
                return issue_reservation(reservation_id=booking.pk, user=actor).issued_at
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            timestamps = list(pool.map(attempt, range(2)))
        self.assertEqual(timestamps[0], timestamps[1])
        self.assertEqual(Reservation.objects.filter(status="issued").count(), 1)
        item.refresh_from_db()
        self.assertEqual(item.status, "rented")
