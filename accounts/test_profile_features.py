from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Product
from .models import Favorite, User


class ProfileFeatureTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="profile-client")
        cls.other = User.objects.create_user(username="other-profile-client", first_name="Bez zmian")
        cls.product = Product.objects.create(name="Ulubione narty", slug="favorite-skis", category="skis", subcategory="downhill", price="100", sale_stock=2)

    def test_profile_saves_only_allowed_fields_on_current_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:edit_profile"), {
            "first_name": "Przykładowe", "last_name": "Konto", "email": "klient@example.com", "phone": "+48 000 000 101",
            "id": self.other.pk, "user_id": self.other.pk, "username": "changed", "is_staff": "on", "is_superuser": "on", "password": "ignored",
        })
        self.assertRedirects(response, reverse("accounts:edit_profile"))
        self.user.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual(self.user.first_name, "Przykładowe")
        self.assertEqual(self.user.email, "klient@example.com")
        self.assertEqual(self.user.phone, "+48 000 000 101")
        self.assertEqual(self.user.username, "profile-client")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.has_usable_password())
        self.assertEqual(self.other.first_name, "Bez zmian")

    def test_profile_validates_email_and_phone_without_partial_save(self):
        self.client.force_login(self.user)
        for fields in ({"email": "błędny"}, {"phone": "telefon"}, {"phone": "1-----1"}, {"phone": "1234567890123456"}):
            response = self.client.post(reverse("accounts:edit_profile"), {"first_name": "Nie zapisywać", **fields})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context["form"].errors)
            self.user.refresh_from_db()
            self.assertEqual(self.user.first_name, "")

    def test_profile_allows_clearing_contact_fields_and_escapes_display(self):
        self.client.force_login(self.user)
        self.client.post(reverse("accounts:edit_profile"), {"first_name": '<script>alert(1)</script>', "email": "klient@example.com"})
        response = self.client.get(reverse("accounts:edit_profile"))
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;')
        self.client.post(reverse("accounts:edit_profile"), {})
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.email, "")

    def test_new_tabs_require_login_and_have_expected_content(self):
        for name in ("edit_profile", "returns", "favorites"):
            url = reverse("accounts:" + name)
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.user)
            self.assertEqual(self.client.get(url).status_code, 200)
            self.client.logout()
        self.client.force_login(self.user)
        response = self.client.get(reverse("accounts:returns"))
        self.assertContains(response, "Nie masz jeszcze zgłoszeń zwrotu")
        self.assertContains(response, "nie można wysłać zgłoszenia")
        self.assertNotContains(response, 'name="order_id"')

    def test_favorites_add_is_idempotent_and_does_not_change_cart_or_stock(self):
        self.client.force_login(self.user)
        url = reverse("accounts:favorite_add", args=[self.product.slug])
        for _ in range(2):
            self.assertRedirects(self.client.post(url), reverse("accounts:favorites"))
        self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)
        self.assertFalse(self.user.cart_items.exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.sale_stock, 2)
        self.assertContains(self.client.get(self.product.get_absolute_url()), "Usuń z ulubionych")
        self.client.logout()
        self.client.force_login(self.user)
        self.assertContains(self.client.get(reverse("accounts:favorites")), self.product.name)

    def test_favorites_are_private_and_remove_cannot_delete_another_users_row(self):
        Favorite.objects.create(user=self.other, product=self.product)
        self.client.force_login(self.user)
        self.assertNotContains(self.client.get(reverse("accounts:favorites")), self.product.name)
        response = self.client.post(reverse("accounts:favorite_remove", args=[self.product.slug]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Favorite.objects.filter(user=self.other).exists())
        self.client.post(reverse("accounts:favorite_add", args=[self.product.slug]))
        self.client.post(reverse("accounts:favorite_remove", args=[self.product.slug]))
        self.assertFalse(Favorite.objects.filter(user=self.user).exists())
        self.assertTrue(Favorite.objects.filter(user=self.other).exists())

    def test_hidden_favorites_are_not_displayed_and_out_of_stock_can_be_saved(self):
        self.client.force_login(self.user)
        self.product.sale_stock = 0
        self.product.save()
        self.client.post(reverse("accounts:favorite_add", args=[self.product.slug]))
        self.assertContains(self.client.get(reverse("accounts:favorites")), self.product.name)
        self.product.is_active = False
        self.product.save()
        self.assertNotContains(self.client.get(reverse("accounts:favorites")), self.product.name)
        self.assertEqual(self.client.post(reverse("accounts:favorite_add", args=[self.product.slug])).status_code, 404)

    def test_favorites_unique_constraint(self):
        Favorite.objects.create(user=self.user, product=self.product)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Favorite.objects.create(user=self.user, product=self.product)

    def test_favorite_writes_require_post_and_all_profile_writes_require_csrf(self):
        self.client.force_login(self.user)
        Favorite.objects.create(user=self.user, product=self.product)
        strict = Client(enforce_csrf_checks=True)
        strict.force_login(self.user)
        for name in ("favorite_add", "favorite_remove"):
            url = reverse("accounts:" + name, args=[self.product.slug])
            self.assertEqual(self.client.get(url).status_code, 405)
            self.assertEqual(strict.post(url).status_code, 403)
            anonymous = Client()
            self.assertEqual(anonymous.post(url).status_code, 302)
        self.assertEqual(strict.post(reverse("accounts:edit_profile"), {"first_name": "Nie zapisywać"}).status_code, 403)
        self.assertEqual(Favorite.objects.count(), 1)


class StoreInformationTests(TestCase):
    def test_public_information_pages_and_footer_links(self):
        for name, expected in (("terms", "Regulamin serwisu Szron"), ("contact", "pomoc@szron.example"), ("stores", "Szron Gliwice")):
            response = self.client.get(reverse("catalog:" + name))
            self.assertContains(response, expected)
            self.assertContains(response, 'aria-label="Informacje o sklepie"')
        response = self.client.get(reverse("catalog:stores"))
        self.assertEqual(len(response.context["stores"]), 4)
        for city in ("Gliwice", "Katowice", "Szczyrk", "Białka Tatrzańska"):
            self.assertContains(response, city)
        self.assertContains(response, "są wymyślone")

    def test_demo_terms_and_contact_do_not_claim_live_orders_or_real_support(self):
        self.assertContains(self.client.get(reverse("catalog:terms")), "Nie przyjmujemy rzeczywistych zamówień")
        self.assertContains(self.client.get(reverse("catalog:contact")), "nie jest działającą infolinią")
