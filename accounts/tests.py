import secrets
from unittest.mock import patch
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404

from catalog.models import Product
from .models import CartItem, User


class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = secrets.token_urlsafe(24)
        cls.customer = User.objects.create_user(username="klient", password=cls.password)
        cls.other = User.objects.create_user(username="inny-klient", password=cls.password)
        cls.admin = User.objects.create_superuser(username="admin-test", password=cls.password)
        cls.product = Product.objects.create(name="Sprzęt testowy", slug="sprzet-testowy", category="skis", subcategory="downhill", price="19.99", sale_stock=5)

    def sign_in(self, user=None, **extra):
        return self.client.post(reverse("accounts:login"), {
            "username": (user or self.customer).username, "password": self.password, **extra,
        })

    def test_shared_login_redirects_according_to_role(self):
        self.assertRedirects(self.sign_in(), reverse("accounts:orders"))
        home = self.client.get(reverse("catalog:home"))
        self.assertContains(home, "Moje konto")
        self.assertNotContains(home, "Panel administratora")
        self.assertRedirects(self.sign_in(self.admin), reverse("admin:index"))
        self.assertContains(self.client.get(reverse("catalog:home")), "Panel administratora")

    def test_login_validates_password_and_inactive_accounts(self):
        response = self.client.post(reverse("accounts:login"), {"username": self.customer.username, "password": secrets.token_urlsafe()})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.customer.is_active = False
        self.customer.save()
        self.assertEqual(self.sign_in().status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_safe_next_returns_to_product_and_external_redirect_is_rejected(self):
        self.assertRedirects(self.sign_in(next=self.product.get_absolute_url()), self.product.get_absolute_url())
        self.assertRedirects(self.sign_in(next="https://example.org/"), reverse("accounts:orders"))
        self.assertRedirects(self.sign_in(next="/admin/"), reverse("accounts:orders"))

    def test_admin_login_uses_shared_form_and_customer_cannot_access_admin(self):
        response = self.client.get("/admin/login/")
        self.assertTemplateUsed(response, "accounts/login.html")
        self.client.force_login(self.customer)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
        response = self.client.post("/admin/login/?next=/admin/", {"username": self.customer.username, "password": self.password, "next": "/admin/"})
        self.assertRedirects(response, reverse("accounts:orders"))

    def test_registration_creates_only_customer_with_hashed_password(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "nowe-konto", "password1": self.password, "password2": self.password,
            "is_staff": "true", "is_superuser": "true",
        })
        self.assertRedirects(response, reverse("accounts:orders"))
        user = User.objects.get(username="nowe-konto")
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_registration_rejects_duplicate_and_mismatched_passwords(self):
        count = User.objects.count()
        for username, second_password in [(self.customer.username, self.password), ("nowy", secrets.token_urlsafe())]:
            response = self.client.post(reverse("accounts:register"), {"username": username, "password1": self.password, "password2": second_password})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
        self.assertEqual(User.objects.count(), count)

    def test_profile_tabs_require_login_and_display_empty_states(self):
        for name in ("orders", "history", "cart"):
            response = self.client.get(reverse("accounts:" + name))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("accounts:login"), response.url)
        self.client.force_login(self.customer)
        for name, expected in [("orders", "Nie masz jeszcze zamówień"), ("history", "historia zakupów jest pusta"), ("cart", "koszyk jest pusty")]:
            response = self.client.get(reverse("accounts:" + name))
            self.assertContains(response, expected)
            self.assertContains(response, 'aria-label="Zakładki konta"')

    def test_logout_is_post_only_and_cart_survives_new_login(self):
        self.client.force_login(self.customer)
        CartItem.objects.create(user=self.customer, product=self.product, quantity=2)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        self.assertIn("_auth_user_id", self.client.session)
        self.assertRedirects(self.client.post(reverse("accounts:logout")), reverse("catalog:home"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.sign_in()
        self.assertContains(self.client.get(reverse("accounts:cart")), self.product.name)

    def test_cart_add_combines_quantity_and_does_not_reduce_stock(self):
        self.client.force_login(self.customer)
        url = reverse("accounts:cart_add", args=[self.product.slug])
        self.assertRedirects(self.client.post(url, {"quantity": 2}), reverse("accounts:cart"))
        self.client.post(url, {"quantity": 1})
        item = CartItem.objects.get(user=self.customer, product=self.product)
        self.assertEqual(item.quantity, 3)
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 5)
        self.assertEqual(self.client.get(reverse("accounts:cart")).context["total"], Decimal("59.97"))

    def test_cart_rejects_invalid_quantities_and_stock_overflow(self):
        self.client.force_login(self.customer)
        url = reverse("accounts:cart_add", args=[self.product.slug])
        for quantity in (0, -1, "abc", "1.5", "", 6, 10**50):
            self.client.post(url, {"quantity": quantity})
            self.assertFalse(CartItem.objects.exists())
        self.client.post(url, {"quantity": 4})
        self.client.post(url, {"quantity": 2})
        self.assertEqual(CartItem.objects.get().quantity, 4)

    def test_cart_rejects_inactive_and_out_of_stock_products(self):
        self.client.force_login(self.customer)
        self.product.sale_stock = 0
        self.product.save()
        url = reverse("accounts:cart_add", args=[self.product.slug])
        self.client.post(url, {"quantity": 1})
        self.assertFalse(CartItem.objects.exists())
        self.product.is_active = False
        self.product.save()
        self.assertEqual(self.client.post(url, {"quantity": 1}).status_code, 404)

    def test_cart_is_private_and_other_users_cannot_change_items(self):
        item = CartItem.objects.create(user=self.other, product=self.product, quantity=2)
        self.client.force_login(self.customer)
        self.assertNotContains(self.client.get(reverse("accounts:cart")), self.product.name)
        self.assertEqual(self.client.post(reverse("accounts:cart_update", args=[item.pk]), {"quantity": 1}).status_code, 404)
        self.assertEqual(self.client.post(reverse("accounts:cart_remove", args=[item.pk])).status_code, 404)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 2)

    def test_cart_update_remove_and_current_price_availability(self):
        self.client.force_login(self.customer)
        item = CartItem.objects.create(user=self.customer, product=self.product)
        url = reverse("accounts:cart_update", args=[item.pk])
        self.client.post(url, {"quantity": 3})
        self.client.post(url, {"quantity": 6})
        self.client.post(url, {"quantity": 0})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)
        self.product.price = Decimal("20.50")
        self.product.sale_stock = 1
        self.product.is_active = False
        self.product.save()
        response = self.client.get(reverse("accounts:cart"))
        self.assertEqual(response.context["total"], Decimal("61.50"))
        self.assertContains(response, "Wybrana ilość jest obecnie niedostępna")
        self.client.post(url, {"quantity": 1})
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)
        self.client.post(reverse("accounts:cart_remove", args=[item.pk]))
        self.assertFalse(CartItem.objects.exists())

    def test_cart_mutations_require_post_login_and_csrf(self):
        item = CartItem.objects.create(user=self.customer, product=self.product)
        urls = [reverse("accounts:cart_add", args=[self.product.slug]), reverse("accounts:cart_update", args=[item.pk]), reverse("accounts:cart_remove", args=[item.pk])]
        for url in urls:
            self.assertEqual(self.client.post(url, {"quantity": 1}).status_code, 302)
        self.client.force_login(self.customer)
        strict_client = Client(enforce_csrf_checks=True)
        strict_client.force_login(self.customer)
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 405)
            self.assertEqual(strict_client.post(url, {"quantity": 1}).status_code, 403)
        self.assertEqual(CartItem.objects.get().quantity, 1)

    def test_database_rejects_zero_quantity_and_duplicate_cart_rows(self):
        CartItem.objects.create(user=self.customer, product=self.product)
        for user, quantity in [(self.other, 0), (self.customer, 1)]:
            with self.assertRaises(IntegrityError), transaction.atomic():
                CartItem.objects.create(user=user, product=self.product, quantity=quantity)

    def test_cart_update_handles_item_deleted_while_waiting_for_product(self):
        self.client.force_login(self.customer)
        item = CartItem.objects.create(user=self.customer, product=self.product, quantity=2)
        first_read = True

        def simulate_other_tab(target, *args, **kwargs):
            nonlocal first_read
            if first_read and getattr(target, "model", target) == CartItem:
                first_read = False
                CartItem.objects.filter(pk=item.pk).delete()
                return item
            return get_object_or_404(target, *args, **kwargs)

        with patch("accounts.views.get_object_or_404", side_effect=simulate_other_tab):
            response = self.client.post(reverse("accounts:cart_update", args=[item.pk]), {"quantity": 3})
        self.assertEqual(response.status_code, 404)
        self.assertFalse(CartItem.objects.filter(pk=item.pk, quantity=3).exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 5)
