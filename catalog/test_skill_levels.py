import importlib
from datetime import timedelta
from io import StringIO
from types import SimpleNamespace

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from orders.models import Order
from rentals.models import RentalItem, Reservation
from rentals.services import issue_reservation, reserve_item
from .demo_data import load_demo_catalogue
from .forms import ProductAdminForm
from .models import Product, SkillLevel


class SkillGuideTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_rental_demo", stdout=StringIO())
        cls.product = Product.objects.get(slug="narty-alpine-172")
        cls.item = RentalItem.objects.filter(product=cls.product).first()
        cls.user = get_user_model().objects.create_user(username="route-buyer")

    def guide(self, code="beginner", **filters):
        return self.client.get(reverse("catalog:skill_level", args=[code]), filters)

    def test_home_links_three_levels_and_all_have_sale_and_rental_choices(self):
        home = self.client.get(reverse("catalog:home"))
        for code in SkillLevel.Code.values:
            self.assertContains(home, reverse("catalog:skill_level", args=[code]))
            page = self.guide(code)
            self.assertContains(page, 'id="buy"')
            self.assertContains(page, 'id="rent"')
            self.assertGreater(len(page.context["products"]), 0)
            self.assertGreater(len(page.context["items"]), 0)
        self.assertEqual(self.guide("expert").status_code, 404)

    def test_model_assignments_exclude_race_from_beginner_and_include_common_protection(self):
        self.assertIn(self.product, self.guide().context["products"])
        self.assertNotIn(Product.objects.get(slug="narty-velocity-165"), self.guide().context["products"])
        self.assertIn(Product.objects.get(slug="narty-velocity-165"), self.guide("advanced").context["products"])
        helmet = Product.objects.filter(category="helmets").first()
        for code in SkillLevel.Code.values:
            self.assertIn(helmet, self.guide(code).context["products"])

    def test_category_filter_applies_to_both_lists_and_handles_empty_and_invalid(self):
        page = self.guide(category="skis")
        self.assertTrue(all(p.category == "skis" for p in page.context["products"]))
        self.assertTrue(all(i.product.category == "skis" for i in page.context["items"]))
        page = self.guide(category="boots")
        self.assertEqual(len(page.context["items"]), 0)
        self.assertContains(page, "Obecnie nie ma gotowych egzemplarzy")
        self.assertEqual(self.guide(category="invalid").context["selected_category"], "")

    def test_hidden_products_and_unassigned_products_never_leak(self):
        self.product.is_active = False
        self.product.save(update_fields=["is_active"])
        page = self.guide()
        self.assertNotIn(self.product, page.context["products"])
        self.assertNotIn(self.item, page.context["items"])
        self.product.is_active = True
        self.product.save(update_fields=["is_active"])
        self.product.skill_levels.clear()
        self.assertNotIn(self.product, self.guide().context["products"])
        self.assertNotIn(self.item, self.guide().context["items"])

    def test_sale_stock_is_independent_from_rentals(self):
        self.product.sale_stock = 0
        self.product.save(update_fields=["sale_stock"])
        page = self.guide()
        self.assertNotIn(self.product, page.context["products"])
        self.assertIn(self.item, page.context["items"])

    def test_hidden_service_and_rented_items_are_not_offered(self):
        for changes in ({"is_active": False}, {"status": "service"}, {"status": "rented"}):
            RentalItem.objects.filter(pk=self.item.pk).update(is_active=True, status="available")
            RentalItem.objects.filter(pk=self.item.pk).update(**changes)
            self.assertNotIn(self.item, self.guide().context["items"])

    def test_outstanding_issue_blocks_item_even_if_status_was_manually_changed(self):
        staff = get_user_model().objects.create_user(username="route-staff", is_staff=True, is_superuser=True)
        today = timezone.localdate()
        reservation = reserve_item(user=self.user, item_id=self.item.pk, start_date=today, end_date=today, quoted_rate=self.item.daily_rate)
        issue_reservation(reservation_id=reservation.pk, user=staff)
        RentalItem.objects.filter(pk=self.item.pk).update(status="available")
        self.assertNotIn(self.item, self.guide().context["items"])

    def test_english_has_translated_levels_content_and_actions(self):
        self.client.cookies["django_language"] = "en"
        for code, label in (("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")):
            page = self.guide(code)
            self.assertContains(page, label)
            self.assertContains(page, "What does this level mean?")
            self.assertContains(page, "Equipment to buy")
            self.assertContains(page, "Details and reservation")
            self.assertNotContains(page, "Początkujący")
            self.assertEqual(page.headers["Content-Language"], "en")

    def test_admin_can_edit_assignments_and_default_seed_preserves_them(self):
        form = ProductAdminForm(instance=self.product)
        self.assertIn("skill_levels", form.fields)
        advanced = SkillLevel.objects.get(code="advanced")
        self.product.skill_levels.set([advanced])
        self.product.price = "123.45"
        self.product.save(update_fields=["price"])
        materials = set(self.product.materials.all())
        call_command("seed_demo", stdout=StringIO())
        self.assertEqual(list(self.product.skill_levels.all()), [advanced])
        call_command("seed_demo", refresh_skills=True, stdout=StringIO())
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.price), "123.45")
        self.assertEqual(set(self.product.materials.all()), materials)
        self.assertEqual(set(self.product.skill_levels.values_list("code", flat=True)), {"beginner", "intermediate"})

    def test_migration_only_classifies_unchanged_demo_and_preserves_existing_assignments(self):
        migration = importlib.import_module("catalog.migrations.0015_assign_demo_skill_levels")
        self.product.skill_levels.clear()
        other = Product.objects.get(slug="narty-alpine-178")
        other.skill_levels.clear()
        other.description = "Własna zmiana administratora"
        other.save(update_fields=["description"])
        custom = Product.objects.create(name="Własny model", slug="route-custom", category="accessories", price="10")
        drift = Product.objects.get(slug="snowboard-drift-156")
        drift.skill_levels.set([SkillLevel.objects.get(code="advanced")])
        migration.assign_levels(apps, SimpleNamespace(connection=connection))
        self.assertEqual(set(self.product.skill_levels.values_list("code", flat=True)), {"beginner", "intermediate"})
        self.assertFalse(other.skill_levels.exists())
        self.assertFalse(custom.skill_levels.exists())
        self.assertEqual(list(drift.skill_levels.values_list("code", flat=True)), ["advanced"])

    def test_demo_assignments_are_explicit_and_new_database_is_populated(self):
        for entry in load_demo_catalogue()["products"]:
            product = Product.objects.get(slug=entry["product"]["slug"])
            self.assertEqual(set(product.skill_levels.values_list("code", flat=True)), set(entry["skill_levels"]))
        self.assertEqual(SkillLevel.objects.count(), 3)

    def test_guide_product_can_be_bought_through_existing_checkout(self):
        page = self.guide(category="skis")
        self.assertContains(page, self.product.get_absolute_url())
        self.client.force_login(self.user)
        detail = self.client.get(self.product.get_absolute_url())
        add_url = reverse("accounts:cart_add", args=[self.product.slug])
        self.assertContains(detail, add_url)
        self.assertEqual(self.client.post(add_url, {"quantity": "1"}).status_code, 302)
        checkout_url = reverse("orders:checkout")
        checkout = self.client.get(checkout_url)
        payload = {"quote": checkout.context["form"]["quote"].value(), "first_name": "Jan", "last_name": "Testowy", "email": "route@example.com", "phone": "500600700", "delivery_method": "pickup", "pickup_location": "gliwice", "accept_demo": "on"}
        self.assertEqual(self.client.post(checkout_url, payload).status_code, 302)
        self.assertEqual(Order.objects.get(user=self.user).lines.get().product, self.product)

    def test_guide_rental_can_be_reserved_after_reading_details(self):
        page = self.guide(category="skis")
        detail_url = reverse("rentals:detail", args=[self.item.pk])
        self.assertContains(page, detail_url)
        self.assertContains(self.client.get(detail_url), self.product.name)
        self.client.force_login(self.user)
        tomorrow = timezone.localdate()+timedelta(days=1)
        reserve_url = reverse("rentals:reserve", args=[self.item.pk])
        dates = {"start_date": tomorrow.isoformat(), "end_date": tomorrow.isoformat()}
        detail = self.client.get(detail_url, dates)
        self.assertContains(detail, reserve_url)
        response = self.client.post(reserve_url, dates | {"quoted_rate": str(self.item.daily_rate)})
        self.assertRedirects(response, reverse("rentals:mine"))
        self.assertEqual(Reservation.objects.get(user=self.user).item, self.item)
