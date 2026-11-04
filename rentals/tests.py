from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.management import call_command, CommandError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from catalog.models import Product
from .models import RentalItem


class RentalFoundationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_rental_demo", stdout=StringIO())

    def test_demo_has_separate_units_and_preserves_sale_stock(self):
        before = dict(Product.objects.values_list("pk", "sale_stock"))
        self.assertEqual(RentalItem.objects.count(), 10)
        self.assertEqual(RentalItem.objects.filter(status="service").count(), 1)
        self.assertEqual(RentalItem.objects.filter(product__slug="narty-alpine-172").count(), 2)
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        item.status = RentalItem.Status.RENTED
        item.save()
        item.delete()
        call_command("seed_rental_demo", stdout=StringIO())
        self.assertEqual(dict(Product.objects.values_list("pk", "sale_stock")), before)

    def test_demo_command_keeps_existing_edits_and_is_repeatable(self):
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        item.daily_rate = Decimal("87.65")
        item.status = RentalItem.Status.SERVICE
        item.is_active = False
        item.size = "180 cm"
        item.technical_notes = "Własna notatka techniczna"
        item.save()
        for _ in range(2):
            call_command("seed_rental_demo", stdout=StringIO())
        item.refresh_from_db()
        self.assertEqual(RentalItem.objects.count(), 10)
        self.assertEqual(item.daily_rate, Decimal("87.65"))
        self.assertEqual(item.status, RentalItem.Status.SERVICE)
        self.assertFalse(item.is_active)
        self.assertEqual(item.size, "180 cm")
        self.assertEqual(item.technical_notes, "Własna notatka techniczna")

    def test_demo_reports_missing_products_without_partial_seed(self):
        RentalItem.objects.all().delete()
        Product.objects.get(slug="snowboard-orbit-152").delete()
        with self.assertRaisesMessage(CommandError, "seed_demo"):
            call_command("seed_rental_demo", stdout=StringIO())
        self.assertFalse(RentalItem.objects.exists())

    def test_database_rejects_invalid_rates_statuses_codes_and_duplicates(self):
        defaults = {"product": Product.objects.first(), "inventory_code": "TEST-001", "size": "M", "daily_rate": Decimal("10.00")}
        for overrides in ({"daily_rate": 0}, {"daily_rate": -1}, {"status": "broken"}, {"inventory_code": ""}, {"inventory_code": "test-001"}, {"inventory_code": "BAD CODE"}):
            with self.subTest(overrides=overrides):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    RentalItem.objects.create(**(defaults | overrides))
        with self.assertRaises(IntegrityError), transaction.atomic():
            RentalItem.objects.create(**(defaults | {"inventory_code": "SZ-N-001"}))

    def test_model_validates_positive_rate_and_required_size(self):
        item = RentalItem.objects.first()
        item.size = ""
        item.daily_rate = Decimal("0.00")
        with self.assertRaises(ValidationError) as error:
            item.full_clean()
        self.assertIn("size", error.exception.message_dict)
        self.assertIn("daily_rate", error.exception.message_dict)

    def test_product_cannot_be_deleted_while_it_has_rental_units(self):
        with self.assertRaises(ProtectedError):
            RentalItem.objects.first().product.delete()

    def test_public_catalogue_is_separate_from_sale_stock(self):
        product = Product.objects.get(slug="narty-alpine-172")
        product.sale_stock = 0
        product.save(update_fields=["sale_stock"])
        response = self.client.get(reverse("rentals:list"))
        self.assertEqual(sum(item.product.name == "Alpine 172" for item in response.context["items"]), 2)
        self.assertContains(response, "65,00 zł")
        self.assertContains(response, "Egzemplarze: 10")
        self.assertContains(response, "Wybierz daty")
        self.assertNotContains(response, "Dodaj do koszyka")

    def test_public_catalogue_hides_inactive_units_products_and_private_notes(self):
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        item.technical_notes = "PRIVATE-SERVICE-NOTE"
        item.save()
        item.product.is_active = False
        item.product.save(update_fields=["is_active"])
        RentalItem.objects.filter(inventory_code="SZ-K-001").update(is_active=False)
        response = self.client.get(reverse("rentals:list"))
        self.assertNotContains(response, "Alpine 172")
        self.assertNotContains(response, "PRIVATE-SERVICE-NOTE")
        self.assertEqual(len(response.context["items"]), 7)

    def test_current_status_is_displayed_without_implying_date_availability(self):
        RentalItem.objects.filter(inventory_code="SZ-N-001").update(status="rented", technical_notes="SECRET-123")
        response = self.client.get(reverse("rentals:list"))
        for text in ("Na stanie", "Do serwisu", "Wypożyczony", "sprawdzić dostępność i cenę"):
            self.assertContains(response, text)
        self.assertNotContains(response, "SECRET-123")

    def test_category_model_size_and_unknown_filters(self):
        url = reverse("rentals:list")
        response = self.client.get(url, {"category": "skis", "model": "narty-alpine-172", "size": "172 cm"})
        self.assertEqual(len(response.context["items"]), 2)
        self.assertContains(response, "Alpine 172")
        self.assertFalse(any(item.product.name == "Drift 156" for item in response.context["items"]))
        response = self.client.get(url, {"category": "unknown"})
        self.assertEqual(len(response.context["items"]), 0)
        self.assertContains(response, "Nie znaleźliśmy sprzętu do wypożyczenia.")

    def test_catalogue_and_admin_labels_are_bilingual(self):
        self.client.cookies["django_language"] = "en"
        response = self.client.get(reverse("rentals:list"))
        for text in ("Rentals", "Items: 10", "Available now", "In service", "65.00 PLN", "day", "Choose dates"):
            self.assertContains(response, text)
        self.assertNotContains(response, ">Wypożyczalnia<")
        with translation.override("en"):
            item = RentalItem.objects.first()
            item.size, item.size_en = "Rozmiar własny", "Custom size"
            self.assertEqual(item.display_size, "Custom size")
            item.size_en = ""
            self.assertEqual(item.display_size, "Rozmiar własny")

    def test_customer_cannot_access_or_change_rental_admin(self):
        user = get_user_model().objects.create_user(username="rental-customer")
        self.client.force_login(user)
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        url = reverse("admin:rentals_rentalitem_change", args=[item.pk])
        response = self.client.post(url, {"status": "rented", "daily_rate": "0.01"})
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, "available")
        self.assertEqual(item.daily_rate, Decimal("65.00"))

    def test_staff_needs_explicit_model_permissions(self):
        user = get_user_model().objects.create_user(username="rental-staff", is_staff=True)
        self.client.force_login(user)
        url = reverse("admin:rentals_rentalitem_changelist")
        self.assertEqual(self.client.get(url).status_code, 403)
        user.user_permissions.add(Permission.objects.get(codename="view_rentalitem"))
        self.assertEqual(self.client.get(url).status_code, 200)
        item = RentalItem.objects.first()
        response = self.client.post(reverse("admin:rentals_rentalitem_change", args=[item.pk]), {"status": "rented"})
        self.assertEqual(response.status_code, 403)

    def test_administrator_can_edit_units_in_both_languages(self):
        user = get_user_model().objects.create_user(username="rental-admin", is_staff=True, is_superuser=True)
        self.client.force_login(user)
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        url = reverse("admin:rentals_rentalitem_change", args=[item.pk])
        self.client.cookies["django_language"] = "en"
        self.assertContains(self.client.get(url), "Daily rate (PLN)")
        response = self.client.post(url, {
            "product": item.product_id, "inventory_code": item.inventory_code,
            "size": item.size, "size_en": item.size_en, "daily_rate": "79.50",
            "status": "service", "is_active": "on", "technical_notes": "Inspection",
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("rentals:list"))
        self.assertContains(response, "79.50 PLN")
        self.assertNotContains(response, "Inspection")
        item.refresh_from_db()
        self.assertEqual(item.status, "service")


    def test_dropdown_options_follow_category_and_model_and_remove_duplicates(self):
        response = self.client.get(reverse("rentals:list"), {"category": "skis"})
        self.assertEqual(response.context["models"], [("narty-alpine-172", "Alpine 172"), ("narty-traverse-84", "Traverse 84")])
        self.assertNotContains(response, 'type="search"')
        self.assertContains(response, '<select id="rental-model" name="model">')
        response = self.client.get(reverse("rentals:list"), {"category": "skis", "model": "narty-alpine-172"})
        self.assertEqual(response.context["sizes"], [("172 cm", "172 cm")])
        self.assertContains(response, 'value="narty-alpine-172" selected')
        self.assertEqual(len(response.context["items"]), 2)

    def test_dropdown_options_exclude_hidden_sale_only_items_and_private_data(self):
        RentalItem.objects.filter(product__slug="narty-alpine-172").update(is_active=False)
        product = Product.objects.get(slug="snowboard-drift-156")
        product.is_active = False
        product.save(update_fields=["is_active"])
        response = self.client.get(reverse("rentals:list"))
        slugs = {row["model"] for row in response.context["rental_options"]}
        self.assertNotIn("narty-alpine-172", slugs)
        self.assertNotIn("snowboard-drift-156", slugs)
        self.assertNotIn("narty-ascend-102", slugs)
        self.assertEqual(len(response.context["rental_options"]), 3)
        for row in response.context["rental_options"]:
            self.assertEqual(set(row), {"category", "model", "name", "size", "size_label"})

    def test_wrong_category_model_or_size_returns_empty_results(self):
        url = reverse("rentals:list")
        for filters in ({"category": "helmets", "model": "narty-alpine-172"}, {"model": "missing"}, {"model": "narty-alpine-172", "size": "200 cm"}):
            with self.subTest(filters=filters):
                response = self.client.get(url, filters)
                self.assertEqual(len(response.context["items"]), 0)
                self.assertContains(response, "brak w tej grupie")

    def test_size_labels_are_translated_but_filter_values_stay_the_same(self):
        RentalItem.objects.filter(inventory_code="SZ-K-001").update(size="Rozmiar własny", size_en="Custom size")
        self.client.cookies["django_language"] = "en"
        response = self.client.get(reverse("rentals:list"), {"category": "helmets", "model": "kask-ridge-m", "size": "Rozmiar własny"})
        self.assertContains(response, "All models")
        self.assertContains(response, "All sizes")
        self.assertContains(response, 'value="Rozmiar własny" selected>Custom size</option>')
        self.assertEqual(len(response.context["items"]), 1)
        self.assertEqual(response.context["items"][0].inventory_code, "SZ-K-001")
