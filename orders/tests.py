from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from threading import Barrier
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, close_old_connections, transaction
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CartItem
from catalog.models import Product
from rentals.models import RentalItem, Reservation
from rentals.services import reserve_item, issue_reservation, return_reservation
from .forms import CheckoutForm
from .models import Order
from .services import change_order_status, make_quote, place_order


def product_for_test(stock=5):
    return Product.objects.create(name="Checkout Alpine", slug="checkout-alpine", category="accessories", description="Demo", description_en="Demo", price="100.01", discount_percent=10, sale_stock=stock, size="M", size_en="M")


def checkout_data(quote="", **overrides):
    return {"first_name": "Jan", "last_name": "Testowy", "email": "buyer@example.com", "phone": "+48 500 600 700", "delivery_method": "pickup", "pickup_location": "gliwice", "accept_demo": "on", "quote": quote, **overrides}


class CheckoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="checkout-buyer", first_name="Jan", email="buyer@example.com")
        cls.other = get_user_model().objects.create_user(username="checkout-other")
        cls.admin = get_user_model().objects.create_user(username="checkout-admin", is_staff=True, is_superuser=True)
        cls.product = product_for_test()

    def setUp(self):
        self.client.force_login(self.user)
        self.line = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.url = reverse("orders:checkout")

    def payload(self, **overrides):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        return checkout_data(response.context["form"]["quote"].value(), **overrides)

    def buy(self, **overrides):
        response = self.client.post(self.url, self.payload(**overrides))
        self.assertEqual(response.status_code, 302, response.context and response.context["form"].errors)
        return Order.objects.get(user=self.user)

    def test_complete_purchase_clears_cart_reduces_stock_and_shows_account_and_confirmation(self):
        rental = RentalItem.objects.create(product=self.product, inventory_code="SALE-SEPARATE-001", size="M", daily_rate="15.00")
        order = self.buy()
        rental.refresh_from_db()
        self.assertEqual(rental.status, "available")
        self.assertEqual(rental.daily_rate, Decimal("15.00"))
        self.assertEqual(order.total, Decimal("180.02"))
        self.assertEqual(order.lines.get().unit_price, Decimal("90.01"))
        self.assertFalse(CartItem.objects.filter(user=self.user).exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 3)
        self.assertContains(self.client.get(order.get_absolute_url()+"?placed=1"), "Dziękujemy")
        self.assertContains(self.client.get(reverse("accounts:orders")), order.number)
        self.assertContains(self.client.get(order.get_absolute_url()), "Checkout Alpine")
        self.assertIn("no-store", self.client.get(order.get_absolute_url()).headers["Cache-Control"])

    def test_courier_cost_and_address_are_validated_and_saved(self):
        order = self.buy(delivery_method="courier", street_address="ul. Testowa 1", postal_code="44-100", city="Gliwice")
        self.assertEqual(order.delivery_fee, Decimal("19.99"))
        self.assertEqual(order.total, Decimal("200.01"))
        self.assertEqual(order.city, "Gliwice")
        self.assertEqual(order.pickup_location, "")
        self.assertEqual(order.pickup_address, "")

    def test_delivery_form_requires_correct_contact_address_and_consent(self):
        for data in (checkout_data(delivery_method="courier"), checkout_data(phone="bad"), checkout_data(accept_demo=""), checkout_data(delivery_method="courier", street_address="Test 1", city="Gliwice", postal_code="abc")):
            data["quote"] = "test"
            self.assertFalse(CheckoutForm(data).is_valid())
        form = CheckoutForm(checkout_data("test", street_address="ignore", city="ignore", postal_code="wrong"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["street_address"], "")

    def test_duplicate_post_is_idempotent_even_with_empty_cart_and_does_not_delete_new_cart(self):
        data = self.payload()
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(CartItem.objects.get(user=self.user).quantity, 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 3)

    def test_changed_price_requires_review_and_new_quote_before_order_is_created(self):
        data = self.payload()
        Product.objects.filter(pk=self.product.pk).update(price="200.00")
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertFalse(Order.objects.exists())
        self.assertEqual(response.context["subtotal"], Decimal("360.00"))
        data["quote"] = response.context["form"]["quote"].value()
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(Order.objects.get().total, Decimal("360.00"))

    def test_quantity_changes_or_forged_quotes_and_owner_are_rejected(self):
        data = self.payload()
        CartItem.objects.filter(pk=self.line.pk).update(quantity=1)
        self.assertEqual(self.client.post(self.url, data).status_code, 200)
        self.assertFalse(Order.objects.exists())
        data = self.payload()
        data["quote"] += "tampered"
        self.assertEqual(self.client.post(self.url, data).status_code, 200)
        self.assertFalse(Order.objects.exists())
        data = self.payload()
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(self.url, data).status_code, 200)
        self.assertFalse(Order.objects.exists())

    def test_stock_failure_is_atomic_for_entire_cart(self):
        second = Product.objects.create(name="Another product", slug="another-checkout", category="accessories", description="Demo", price="30.00", sale_stock=1)
        CartItem.objects.create(user=self.user, product=second, quantity=1)
        data = self.payload()
        Product.objects.filter(pk=second.pk).update(sale_stock=0)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 5)
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 2)

    def test_cancel_restocks_once_and_is_private_and_post_only(self):
        order = self.buy()
        url = reverse("orders:cancel", args=[order.reference])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(order.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.post(url).status_code, 404)
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.assertEqual(self.client.post(url).status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 5)
        self.assertContains(self.client.get(reverse("accounts:history")), order.number)
        self.assertNotContains(self.client.get(reverse("accounts:orders")), order.number)

    def test_customer_cannot_modify_processing_order_and_admin_stages_go_to_history(self):
        order = self.buy()
        for status in (Order.Status.PREPARING, Order.Status.READY, Order.Status.COMPLETED):
            if status == Order.Status.PREPARING:
                with self.assertRaises(PermissionDenied):
                    change_order_status(reference=order.reference, user=self.user, target=status)
            order = change_order_status(reference=order.reference, user=self.admin, target=status, as_staff=True)
            if status == Order.Status.PREPARING:
                with self.assertRaises(ValidationError):
                    change_order_status(reference=order.reference, user=self.user, target=Order.Status.CANCELLED)
        self.assertIsNotNone(order.completed_at)
        self.assertContains(self.client.get(reverse("accounts:history")), order.number)
        self.assertNotContains(self.client.get(reverse("accounts:orders")), order.number)

    def test_shipping_stage_is_checked_and_post_completion_cannot_cancel(self):
        order = self.buy(delivery_method="courier", street_address="Test 1", postal_code="44-100", city="Gliwice")
        change_order_status(reference=order.reference, user=self.admin, target=Order.Status.PREPARING, as_staff=True)
        with self.assertRaises(ValidationError):
            change_order_status(reference=order.reference, user=self.admin, target=Order.Status.READY, as_staff=True)
        change_order_status(reference=order.reference, user=self.admin, target=Order.Status.SHIPPED, as_staff=True)
        with self.assertRaises(ValidationError):
            change_order_status(reference=order.reference, user=self.admin, target=Order.Status.CANCELLED, as_staff=True)
        change_order_status(reference=order.reference, user=self.admin, target=Order.Status.COMPLETED, as_staff=True)

    def test_order_keeps_price_name_size_and_address_snapshot(self):
        order = self.buy(notes="<script>alert(1)</script>")
        Product.objects.filter(pk=self.product.pk).update(price="1.00", name="Changed", size="XL", is_active=False)
        line = order.lines.get()
        self.assertEqual(line.product_name, "Checkout Alpine")
        self.assertEqual(line.size, "M")
        self.assertEqual(line.unit_price, Decimal("90.01"))
        response = self.client.get(order.get_absolute_url())
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")
        self.assertContains(self.client.get(reverse("accounts:orders")), "Checkout Alpine")

    def test_checkout_and_cancellation_enforce_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url, self.payload()).status_code, 403)
        order = self.buy()
        self.assertEqual(client.post(reverse("orders:cancel", args=[order.reference])).status_code, 403)

    def test_admin_status_action_and_readonly_history(self):
        order = self.buy()
        self.client.force_login(self.admin)
        url = reverse("admin:orders_order_changelist")
        self.assertEqual(self.client.post(url, {"action": "prepare_selected", "_selected_action": [order.pk]}).status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, "preparing")
        self.assertEqual(self.client.post(reverse("admin:orders_order_change", args=[order.pk]), {"status": "completed"}).status_code, 403)
        self.assertEqual(self.client.get(reverse("admin:orders_order_add")).status_code, 403)
        limited = get_user_model().objects.create_user(username="limited-orders", is_staff=True)
        limited.user_permissions.add(Permission.objects.get(codename="change_order"))
        self.client.force_login(limited)
        self.assertNotContains(self.client.get(url), 'value="prepare_selected"')

    def test_database_rejects_bad_totals_status_and_quantity(self):
        order = self.buy()
        for changes in ({"total": "0.01"}, {"status": "invented"}, {"delivery_fee": "-1.00"}):
            with self.assertRaises(IntegrityError), transaction.atomic():
                Order.objects.filter(pk=order.pk).update(**changes)
        with self.assertRaises(IntegrityError), transaction.atomic():
            order.lines.update(quantity=0)

    def test_english_checkout_and_confirmation(self):
        self.client.cookies["django_language"] = "en"
        response = self.client.get(self.url)
        for text in ("Complete your order", "Your details", "Order summary", "Place order", "180.02 PLN"):
            self.assertContains(response, text)
        order = self.buy()
        self.assertContains(self.client.get(order.get_absolute_url()), "Accepted")


    def test_service_validates_contact_and_delivery_data(self):
        data = self.payload()
        with self.assertRaises(ValidationError):
            place_order(user=self.user, data=checkout_data(email="bad-email", delivery_method="courier"), quote=data["quote"])
        self.assertFalse(Order.objects.exists())



    def test_valid_csrf_checkout_survives_logout_and_new_login(self):
        client=Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        response=client.get(self.url)
        data=checkout_data(response.context["form"]["quote"].value(),csrfmiddlewaretoken=client.cookies["csrftoken"].value)
        self.assertEqual(client.post(self.url,data).status_code,302)
        order=Order.objects.get(user=self.user)
        self.assertContains(client.get(order.get_absolute_url()),order.number)
        client.post(reverse("accounts:logout"),{"csrfmiddlewaretoken":client.cookies["csrftoken"].value})
        self.assertEqual(client.get(order.get_absolute_url()).status_code,302)
        client.force_login(self.user)
        self.assertContains(client.get(reverse("accounts:orders")),order.number)



class RentalAccountRegressionTests(TestCase):
    def test_reservation_is_visible_in_default_account_after_login_hidden_product_issue_and_return(self):
        customer = get_user_model().objects.create_user(username="reservation-dashboard")
        other = get_user_model().objects.create_user(username="reservation-other")
        staff = get_user_model().objects.create_user(username="reservation-staff", is_staff=True, is_superuser=True)
        product = product_for_test()
        item = RentalItem.objects.create(product=product, inventory_code="ACCOUNT-001", size="M", daily_rate="30.00")
        today = timezone.localdate()
        reservation = reserve_item(user=customer, item_id=item.pk, start_date=today, end_date=today+timedelta(days=2), quoted_rate=Decimal("30.00"))
        self.client.force_login(customer)
        response = self.client.get(reverse("accounts:profile"), follow=True)
        self.assertContains(response, reservation.product_name)
        self.assertContains(response, "Rezerwacja")
        self.assertIn("no-store", response.headers["Cache-Control"])
        issue_reservation(reservation_id=reservation.pk, user=staff)
        self.assertContains(self.client.get(reverse("accounts:orders")), "Wypożyczony")
        product.is_active = False
        product.save(update_fields=["is_active"])
        self.assertContains(self.client.get(reverse("accounts:orders")), reservation.product_name)
        self.client.post(reverse("accounts:logout"))
        self.client.force_login(customer)
        self.assertContains(self.client.get(reverse("accounts:orders")), reservation.product_name)
        return_reservation(reservation_id=reservation.pk, user=staff)
        self.assertContains(self.client.get(reverse("accounts:history")), reservation.product_name)
        self.assertContains(self.client.get(reverse("rentals:mine")), reservation.product_name)
        self.client.force_login(other)
        self.assertNotContains(self.client.get(reverse("accounts:orders")), reservation.product_name)
        self.assertNotContains(self.client.get(reverse("accounts:history")), reservation.product_name)
        self.assertNotContains(self.client.get(reverse("rentals:mine")), reservation.product_name)


class ConcurrentPurchaseTests(TransactionTestCase):
    def test_two_customers_cannot_buy_the_last_item(self):
        product = product_for_test(stock=1)
        users = [get_user_model().objects.create_user(username=f"stock-buyer-{i}") for i in range(2)]
        quotes = []
        for user in users:
            CartItem.objects.create(user=user, product=product, quantity=1)
            quotes.append(make_quote(user, list(CartItem.objects.filter(user=user).select_related("product"))))
        barrier = Barrier(2)
        def buy(index):
            close_old_connections()
            try:
                user = get_user_model().objects.get(pk=users[index].pk)
                barrier.wait(timeout=10)
                try:
                    place_order(user=user, data=checkout_data(), quote=quotes[index])
                except ValidationError:
                    return "unavailable"
                return "ordered"
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(buy, range(2)))
        self.assertCountEqual(results, ["ordered", "unavailable"])
        product.refresh_from_db()
        self.assertEqual(product.sale_stock, 0)
        self.assertEqual(Order.objects.count(), 1)

    def test_simultaneous_duplicate_checkout_does_not_charge_stock_twice(self):
        product = product_for_test(stock=2)
        user = get_user_model().objects.create_user(username="same-order-buyer")
        CartItem.objects.create(user=user, product=product, quantity=1)
        quote = make_quote(user, list(CartItem.objects.filter(user=user).select_related("product")))
        barrier = Barrier(2)
        def buy(_):
            close_old_connections()
            try:
                actor = get_user_model().objects.get(pk=user.pk)
                barrier.wait(timeout=10)
                return place_order(user=actor, data=checkout_data(), quote=quote).pk
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            ids = list(pool.map(buy, range(2)))
        self.assertEqual(ids[0], ids[1])
        product.refresh_from_db()
        self.assertEqual(product.sale_stock, 1)
        self.assertEqual(Order.objects.count(), 1)


    def test_simultaneous_cancellations_restock_only_once(self):
        product=product_for_test(stock=5)
        user=get_user_model().objects.create_user(username="cancel-buyer")
        CartItem.objects.create(user=user,product=product,quantity=2)
        quote=make_quote(user,list(CartItem.objects.filter(user=user).select_related("product")))
        order=place_order(user=user,data=checkout_data(),quote=quote)
        barrier=Barrier(2)
        def attempt(_):
            close_old_connections()
            try:
                actor=get_user_model().objects.get(pk=user.pk)
                barrier.wait(timeout=10)
                return change_order_status(reference=order.reference,user=actor,target=Order.Status.CANCELLED).cancelled_at
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(attempt,range(2)))
        self.assertEqual(results[0],results[1])
        product.refresh_from_db()
        self.assertEqual(product.sale_stock,5)
