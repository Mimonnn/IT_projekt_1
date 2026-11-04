from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from threading import Barrier

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, close_old_connections, transaction
from django.db.models.deletion import ProtectedError
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import Product
from .forms import RentalDatesForm
from .models import RentalItem, Reservation
from .services import cancel_reservation, reserve_item


def create_equipment():
    product = Product.objects.create(name="Booking demo", slug="booking-demo", category="accessories", description="Demo", price="100.00", sale_stock=7, size="M")
    return RentalItem.objects.create(product=product, inventory_code="BOOK-001", size="M", size_en="M", daily_rate="25.50")


class ReservationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="booking-client")
        cls.other = get_user_model().objects.create_user(username="other-client")
        cls.item = create_equipment()

    def setUp(self):
        self.start = timezone.localdate() + timedelta(days=5)
        self.end = self.start + timedelta(days=2)
        self.client.force_login(self.user)

    def reserve(self, **overrides):
        return reserve_item(**({"user": self.user, "item_id": self.item.pk, "start_date": self.start, "end_date": self.end, "quoted_rate": Decimal("25.50")} | overrides))

    def dates(self, **extra):
        return {"start_date": self.start.isoformat(), "end_date": self.end.isoformat(), **extra}

    def test_preview_confirm_account_cancel_and_book_again(self):
        url = reverse("rentals:reserve", args=[self.item.pk])
        response = self.client.get(url, self.dates())
        self.assertContains(response, "76,50")
        self.assertContains(response, "Potwierdź rezerwację")
        self.assertContains(response, f'data-start-date="{self.start.isoformat()}"')
        self.assertContains(response, f'data-end-date="{self.end.isoformat()}"')
        self.assertContains(response, "js/reservation-confirm.js?v=1")
        self.assertFalse(Reservation.objects.exists())
        response = self.client.post(url, self.dates(quoted_rate="25.50"))
        self.assertRedirects(response, reverse("rentals:mine"))
        reservation = Reservation.objects.get()
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.days, 3)
        self.assertEqual(reservation.total_price, Decimal("76.50"))
        self.assertContains(self.client.get(reverse("rentals:mine")), "Booking demo")
        response = self.client.post(reverse("rentals:cancel", args=[reservation.pk]))
        self.assertRedirects(response, reverse("rentals:mine"))
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, "cancelled")
        self.assertIsNotNone(reservation.cancelled_at)
        self.assertNotEqual(self.reserve().pk, reservation.pk)
        self.item.product.refresh_from_db()
        self.assertEqual(self.item.product.sale_stock, 7)

    def test_dates_validate_past_reversed_missing_and_invalid_values(self):
        for data in ({"start_date": "garbage", "end_date": self.end}, {"start_date": self.start}, {"start_date": self.start, "end_date": self.start - timedelta(days=1)}, {"start_date": timezone.localdate()-timedelta(days=1), "end_date": self.end}):
            with self.subTest(data=data):
                self.assertFalse(RentalDatesForm(data).is_valid())
        reservation = self.reserve(start_date=timezone.localdate(), end_date=timezone.localdate())
        self.assertEqual(reservation.days, 1)
        self.assertEqual(reservation.total_price, Decimal("25.50"))

    def test_service_also_rejects_invalid_dates(self):
        with self.assertRaises(ValidationError):
            self.reserve(end_date=self.start-timedelta(days=1))
        self.assertFalse(Reservation.objects.exists())

    def test_partial_enclosing_and_boundary_overlaps_are_blocked(self):
        self.reserve()
        for start, end in ((self.start, self.end), (self.start-timedelta(days=1), self.start), (self.end, self.end+timedelta(days=2)), (self.start-timedelta(days=1), self.end+timedelta(days=1))):
            with self.subTest(start=start, end=end):
                with self.assertRaises(ValidationError):
                    self.reserve(user=self.other, start_date=start, end_date=end)
        self.assertEqual(Reservation.objects.count(), 1)
        self.reserve(user=self.other, start_date=self.end+timedelta(days=1), end_date=self.end+timedelta(days=1))
        self.assertEqual(Reservation.objects.count(), 2)

    def test_other_physical_item_is_available_for_same_dates(self):
        self.reserve()
        second = RentalItem.objects.create(product=self.item.product, inventory_code="BOOK-002", size="M", daily_rate="25.50")
        self.reserve(user=self.other, item_id=second.pk)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_repeated_confirmation_does_not_duplicate_reservation(self):
        booking = self.reserve()
        self.assertEqual(self.reserve().pk, booking.pk)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_nonavailable_and_hidden_equipment_cannot_be_reserved(self):
        for changes in ({"status": "service"}, {"status": "rented"}, {"is_active": False}):
            with self.subTest(changes=changes):
                RentalItem.objects.filter(pk=self.item.pk).update(status="available", is_active=True)
                RentalItem.objects.filter(pk=self.item.pk).update(**changes)
                with self.assertRaises(ValidationError):
                    self.reserve()
        RentalItem.objects.filter(pk=self.item.pk).update(status="available", is_active=True)
        Product.objects.filter(pk=self.item.product_id).update(is_active=False)
        with self.assertRaises(ValidationError):
            self.reserve()

    def test_catalogue_filters_dates_and_calculates_period_price(self):
        self.reserve()
        response = self.client.get(reverse("rentals:list"), self.dates())
        self.assertEqual(response.context["items"], [])
        response = self.client.get(reverse("rentals:list"), {"start_date": (self.end+timedelta(days=1)).isoformat(), "end_date": (self.end+timedelta(days=2)).isoformat()})
        self.assertEqual(len(response.context["items"]), 1)
        self.assertContains(response, "51,00")
        self.assertContains(response, "start_date=")

    def test_invalid_catalogue_dates_do_not_offer_confirmation_links(self):
        response = self.client.get(reverse("rentals:list"), {"start_date": "wrong"})
        self.assertTrue(response.context["date_form"].errors)
        self.assertNotContains(response, reverse("rentals:reserve", args=[self.item.pk]))

    def test_customer_cannot_see_or_cancel_another_customers_reservation(self):
        reservation = self.reserve(user=self.other)
        self.assertNotContains(self.client.get(reverse("rentals:mine")), "Booking demo")
        self.assertEqual(self.client.post(reverse("rentals:cancel", args=[reservation.pk])).status_code, 404)
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, "confirmed")

    def test_anonymous_login_and_get_requests_never_create_or_cancel(self):
        self.client.logout()
        url = reverse("rentals:reserve", args=[self.item.pk])
        self.assertEqual(self.client.get(url, self.dates()).status_code, 302)
        self.assertEqual(self.client.post(url, self.dates(quoted_rate="25.50")).status_code, 302)
        self.assertFalse(Reservation.objects.exists())
        self.client.force_login(self.user)
        booking = self.reserve()
        self.assertEqual(self.client.get(reverse("rentals:cancel", args=[booking.pk])).status_code, 405)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "confirmed")

    def test_confirm_and_cancel_require_csrf(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        url = reverse("rentals:reserve", args=[self.item.pk])
        self.assertEqual(csrf_client.post(url, self.dates(quoted_rate="25.50")).status_code, 403)
        booking = self.reserve()
        self.assertEqual(csrf_client.post(reverse("rentals:cancel", args=[booking.pk])).status_code, 403)

    def test_rate_and_personal_fields_cannot_be_forged(self):
        url = reverse("rentals:reserve", args=[self.item.pk])
        response = self.client.post(url, self.dates(quoted_rate="0.01", user=self.other.pk, total_price="0.01"))
        self.assertContains(response, "Stawka zmieniła się")
        self.assertFalse(Reservation.objects.exists())
        response = self.client.post(url, self.dates(quoted_rate="25.50", user=self.other.pk, total_price="0.01"))
        self.assertEqual(response.status_code, 302)
        booking = Reservation.objects.get()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.total_price, Decimal("76.50"))

    def test_rate_change_after_preview_requires_new_check_and_history_keeps_snapshot(self):
        booking = self.reserve()
        RentalItem.objects.filter(pk=self.item.pk).update(daily_rate="80.00", size="XL")
        Product.objects.filter(pk=self.item.product_id).update(name="Renamed equipment")
        booking.refresh_from_db()
        self.assertEqual(booking.total_price, Decimal("76.50"))
        self.assertEqual(booking.product_name, "Booking demo")
        self.assertEqual(booking.size, "M")
        with self.assertRaises(ValidationError):
            self.reserve(start_date=self.end+timedelta(days=1), end_date=self.end+timedelta(days=2))

    def test_past_reservation_cannot_be_cancelled_and_cancel_is_idempotent(self):
        booking = self.reserve()
        Reservation.objects.filter(pk=booking.pk).update(start_date=timezone.localdate()-timedelta(days=1))
        with self.assertRaises(ValidationError):
            cancel_reservation(reservation_id=booking.pk, user=self.user)
        Reservation.objects.filter(pk=booking.pk).update(start_date=self.start)
        cancel_reservation(reservation_id=booking.pk, user=self.user)
        cancelled = Reservation.objects.get(pk=booking.pk).cancelled_at
        cancel_reservation(reservation_id=booking.pk, user=self.user)
        self.assertEqual(Reservation.objects.get(pk=booking.pk).cancelled_at, cancelled)

    def test_database_rejects_invalid_dates_rate_status_and_protects_history(self):
        booking = self.reserve()
        for changes in ({"end_date": self.start-timedelta(days=1)}, {"daily_rate": "0.00"}, {"status": "fake"}):
            with self.subTest(changes=changes):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Reservation.objects.filter(pk=booking.pk).update(**changes)
        with self.assertRaises(ProtectedError):
            self.item.delete()
        with self.assertRaises(ProtectedError):
            self.user.delete()

    def test_english_booking_and_account_workflow(self):
        self.client.cookies["django_language"] = "en"
        response = self.client.get(reverse("rentals:reserve", args=[self.item.pk]), self.dates())
        for text in ("Confirm reservation", "76.50 PLN", "Pickup date", "Return date"):
            self.assertContains(response, text)
        self.reserve()
        response = self.client.get(reverse("rentals:mine"))
        for text in ("My rentals", "Reserved", "Cancel reservation", "76.50 PLN"):
            self.assertContains(response, text)

    def test_administrator_cannot_bypass_workflow_with_direct_edit_or_delete(self):
        admin = get_user_model().objects.create_user(username="booking-admin", is_staff=True, is_superuser=True)
        self.client.force_login(admin)
        booking = self.reserve()
        response = self.client.post(reverse("admin:rentals_reservation_change", args=[booking.pk]), {"status": "cancelled", "daily_rate": "0.01"})
        self.assertEqual(response.status_code, 403)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "confirmed")
        self.assertEqual(booking.daily_rate, Decimal("25.50"))
        self.assertEqual(self.client.get(reverse("admin:rentals_reservation_add")).status_code, 403)
        self.assertEqual(self.client.post(reverse("admin:rentals_reservation_delete", args=[booking.pk])).status_code, 403)
        response = self.client.post(reverse("admin:rentals_reservation_changelist"), {"action": "cancel_selected", "_selected_action": [booking.pk]})
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")


    def test_service_normalizes_validated_dates(self):
        booking = self.reserve(start_date=self.start.isoformat(), end_date=self.end.isoformat())
        self.assertEqual(booking.days, 3)
        self.assertEqual(booking.start_date, self.start)

    def test_navigation_highlights_the_correct_section(self):
        response = self.client.get(reverse("rentals:mine"))
        self.assertContains(response, '<a href="/konto/" aria-current="page">Moje konto</a>', html=True)
        self.assertNotContains(response, '<a href="/wypozyczalnia/" aria-current="page">Wypożyczalnia</a>', html=True)
        response = self.client.get(reverse("rentals:list"))
        self.assertNotContains(response, '<a href="/katalog/" aria-current="page">Sprzęt</a>', html=True)


class ConcurrentReservationTests(TransactionTestCase):
    def test_two_customers_cannot_book_same_item_simultaneously(self):
        item = create_equipment()
        users = [get_user_model().objects.create_user(username=f"concurrent-{i}") for i in range(2)]
        barrier = Barrier(2)
        start = timezone.localdate()+timedelta(days=10)
        def attempt(user_id):
            close_old_connections()
            try:
                user = get_user_model().objects.get(pk=user_id)
                barrier.wait(timeout=10)
                try:
                    reserve_item(user=user, item_id=item.pk, start_date=start, end_date=start, quoted_rate=Decimal("25.50"))
                except ValidationError:
                    return "unavailable"
                return "reserved"
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, [user.pk for user in users]))
        self.assertCountEqual(results, ["reserved", "unavailable"])
        self.assertEqual(Reservation.objects.count(), 1)
