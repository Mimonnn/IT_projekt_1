from io import StringIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from .forms import ProductAdminForm
from .models import Product
from .taxonomy import SUBCATEGORIES


class CategorySubcategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for category, choices in SUBCATEGORIES.items():
            for code, _ in choices:
                Product.objects.create(name=f"Sprzęt {category} {code}", slug=f"{category}-{code}",
                                       category=category, subcategory=code, description="Testowy sprzęt", price="100")

    def test_every_category_and_subcategory_filters_its_own_products(self):
        home = self.client.get(reverse("catalog:home"))
        for category, choices in SUBCATEGORIES.items():
            for code, label in choices:
                with self.subTest(category=category, code=code):
                    self.assertContains(home, f"?category={category}&amp;subcategory={code}")
                    response = self.client.get(reverse("catalog:list"), {
                        "category": category, "subcategory": code, "q": "Sprzęt",
                    })
                    product = response.context["products"].get()
                    self.assertEqual((product.category, product.subcategory), (category, code))
                    self.assertEqual(product.get_subcategory_display(), label)
                    product.full_clean()
                    self.assertContains(response, f'<option value="{code}" selected>')
                    self.assertContains(self.client.get(product.get_absolute_url()), label)

    def test_all_seven_menu_buttons_have_unique_panel_ids(self):
        response = self.client.get(reverse("catalog:home"))
        self.assertContains(response, 'class="ski-menu-trigger"', count=7)
        for category in SUBCATEGORIES:
            self.assertContains(response, f'aria-controls="submenu-{category}"', count=1)
            self.assertContains(response, f'id="submenu-{category}"', count=1)

    def test_category_without_subcategories_ignores_stale_filter(self):
        product = Product.objects.create(name="Akcesorium", slug="akcesorium", category="accessories", price="10")
        response = self.client.get(reverse("catalog:list"), {"category": "accessories", "subcategory": "otg"})
        self.assertEqual(list(response.context["products"]), [product])
        self.assertContains(response, 'id="subcategory" disabled')

    def test_old_ski_urls_keep_working(self):
        old = self.client.get(reverse("catalog:list"), {"category": "skis", "ski_subcategory": "race"})
        new = self.client.get(reverse("catalog:list"), {"category": "skis", "subcategory": "race"})
        self.assertEqual(list(old.context["products"]), list(new.context["products"]))

    def test_models_and_database_reject_wrong_pairs(self):
        for category in [*SUBCATEGORIES, "accessories"]:
            with self.subTest(category=category):
                product = Product(name="Błędny", slug="bledny", category=category,
                                  subcategory="not_a_type", description="Test", price="100")
                with self.assertRaises(ValidationError):
                    product.full_clean()
                with self.assertRaises(IntegrityError), transaction.atomic():
                    product.save()
        product = Product.objects.get(category="goggles", subcategory="otg")
        for value in ("", "race"):
            product.subcategory = value
            with self.assertRaises(ValidationError):
                product.full_clean()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.filter(pk=product.pk).update(subcategory="race")

    def test_admin_options_follow_category_and_save_all_categories(self):
        user = get_user_model().objects.create_superuser(username="category-admin")
        self.client.force_login(user)
        for category, choices in SUBCATEGORIES.items():
            with self.subTest(category=category):
                code, _ = choices[-1]
                product = Product.objects.filter(category=category).first()
                form = ProductAdminForm(instance=product)
                self.assertEqual(form.fields["subcategory"].choices, [("", "---------"), *choices])
                response = self.client.post(reverse("admin:catalog_product_change", args=[product.pk]), {
                    "name": product.name, "slug": product.slug, "category": category,
                    "subcategory": code, "description": "Test", "price": "123.45",
                    "sale_stock": 2, "is_active": "on",
                })
                self.assertEqual(response.status_code, 302)
                product.refresh_from_db()
                self.assertEqual(product.subcategory, code)
        form = ProductAdminForm(data={"category": "goggles", "subcategory": "race"})
        self.assertFalse(form.is_valid())
        self.assertIn("subcategory", form.errors)

    def test_seed_preserves_existing_types_in_other_categories(self):
        call_command("seed_demo", stdout=StringIO())
        snowboard = Product.objects.get(slug="snowboard-drift-156")
        self.assertEqual(snowboard.subcategory, "all_mountain")
        snowboard.subcategory = "carving"
        snowboard.save()
        call_command("seed_demo", stdout=StringIO())
        snowboard.refresh_from_db()
        self.assertEqual(snowboard.subcategory, "carving")


class AdminReadinessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username="readiness-admin")
        self.client.force_login(self.user)
        self.product = Product.objects.create(name="Starsze buty", slug="starsze-buty", category="boots", price="100")

    def test_admin_script_url_keeps_query_separate_from_filename(self):
        response = self.client.get(reverse("admin:catalog_product_change", args=[self.product.pk]))
        self.assertContains(response, 'src="/static/js/admin-subcategories.js?v=1"')
        self.assertNotContains(response, 'admin-subcategories.js%3F')

    def test_feature_order_can_be_changed_for_legacy_product(self):
        response = self.client.post(reverse("admin:catalog_product_changelist"), {
            "form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "1", "form-MAX_NUM_FORMS": "1000",
            "form-0-id": self.product.pk, "form-0-featured_order": "2", "_save": "Zapisz",
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.featured_order, 2)


class SubcategoryMigrationTests(TransactionTestCase):
    def test_rename_preserves_ski_types_and_only_classifies_known_snowboard(self):
        old_target = [("catalog", "0007_categorize_demo_skis")]
        new_target = [("catalog", "0009_categorize_demo_snowboard")]
        executor = MigrationExecutor(connection)
        try:
            executor.migrate(old_target)
            old_model = executor.loader.project_state(old_target).apps.get_model("catalog", "Product")
            old_model.objects.create(name="Własne narty", slug="wlasne", category="skis",
                                     ski_subcategory="race", price="321.50", sale_stock=7)
            old_model.objects.create(name="Narty bez typu", slug="bez-typu", category="skis", price="50")
            old_model.objects.create(name="Drift", slug="snowboard-drift-156", category="snowboards",
                                     price="200", description="Snowboard all-mountain o długości 156 cm.")
            old_model.objects.create(name="Inna deska", slug="inna-deska", category="snowboards", price="100")
            executor = MigrationExecutor(connection)
            executor.migrate(new_target)
            new_model = executor.loader.project_state(new_target).apps.get_model("catalog", "Product")
            product = new_model.objects.get(slug="wlasne")
            self.assertEqual(product.subcategory, "race")
            self.assertEqual(str(product.price), "321.50")
            self.assertEqual(product.sale_stock, 7)
            self.assertEqual(new_model.objects.get(slug="bez-typu").subcategory, "")
            self.assertEqual(new_model.objects.get(slug="inna-deska").subcategory, "")
            self.assertEqual(new_model.objects.get(slug="snowboard-drift-156").subcategory, "all_mountain")
        finally:
            MigrationExecutor(connection).migrate(new_target)
