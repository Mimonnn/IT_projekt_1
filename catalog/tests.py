from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Product


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Testowe narty", slug="testowe-narty", category="skis",
            description="Sprzęt testowy", price="1250.00", sale_stock=4,
        )
        cls.hidden = Product.objects.create(
            name="Ukryty produkt", slug="ukryty", category="boots",
            description="Niepublikowany", price="100.00", is_active=False,
        )

    def test_home_and_catalog_read_database(self):
        self.product.image_path = "img/narty.jpg"
        self.product.featured_order = 1
        self.product.save()
        for url in (reverse("catalog:home"), reverse("catalog:list")):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, self.product.name)
                self.assertContains(response, "1250,00 zł")
                self.assertNotContains(response, self.hidden.name)
        self.assertContains(self.client.get(reverse("catalog:list")), "Dostępne: 4 szt.")

    def test_detail_has_current_price_and_stock(self):
        self.product.price = Decimal("999.99")
        self.product.sale_stock = 2
        self.product.save()
        response = self.client.get(self.product.get_absolute_url())
        self.assertContains(response, "999,99 zł")
        self.assertContains(response, "Na sprzedaż: 2 szt.")

    def test_showcase_is_selected_ordered_and_links_to_current_offers(self):
        self.product.image_path = "img/narty.jpg"
        self.product.featured_order = 2
        self.product.save()
        first = Product.objects.create(
            name="Wyróżniony snowboard", slug="wyrozniony", category="snowboards",
            description="Test", price="555.00", image_path="img/snowboard1.jpg", featured_order=1,
        )
        Product.objects.create(name="Bez zdjęcia", slug="bez-zdjecia", category="skis",
                               price="10", featured_order=0)
        self.hidden.image_path = "img/narty.jpg"
        self.hidden.featured_order = 0
        self.hidden.save()
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(list(response.context["featured_products"]), [first, self.product])
        self.assertContains(response, 'href="' + first.get_absolute_url() + '"')
        self.assertContains(response, "/static/img/snowboard1.jpg")
        self.assertContains(response, "555,00 zł")
        self.assertNotContains(response, "Bez zdjęcia")

    def test_showcase_limit_and_empty_fallback(self):
        response = self.client.get(reverse("catalog:home"))
        self.assertNotContains(response, 'class="showcase-grid"')
        self.assertContains(response, "Wszystko zaczyna się")
        for index in range(4):
            Product.objects.create(name=f"Wybrany {index}", slug=f"wybrany-{index}",
                                   category="skis", price="10", image_path="img/narty.jpg",
                                   featured_order=index)
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(len(response.context["featured_products"]), 3)

    def test_product_photo_is_shared_by_catalog_and_detail(self):
        self.product.image_path = "img/narty.jpg"
        self.product.save()
        for url in (reverse("catalog:list"), self.product.get_absolute_url()):
            self.assertContains(self.client.get(url), "/static/img/narty.jpg")
        for path in ("../secret.jpg", "https://example.com/photo.jpg", "img/../photo.jpg"):
            self.product.image_path = path
            with self.assertRaises(ValidationError):
                self.product.full_clean()

    def test_panorama_and_category_links_work_without_featured_products(self):
        response = self.client.get(reverse("catalog:home"))
        for index in range(1, 5):
            self.assertContains(response, f"/static/img/hero/panorama{index}.jpg")
        categories = [category for category in Product.Category if category != Product.Category.ACCESSORIES]
        self.assertEqual(len(response.context["hero_categories"]), 7)
        for category in categories:
            with self.subTest(category=category):
                product = Product.objects.create(name=f"Sprzęt {category}", slug=f"sprzet-{category}",
                                                 category=category, price="100")
                self.assertContains(response, f'?category={category}')
                filtered = self.client.get(reverse("catalog:list"), {"category": category})
                self.assertIn(product, filtered.context["products"])
                self.assertTrue(all(item.category == category for item in filtered.context["products"]))
                detail = self.client.get(product.get_absolute_url())
                self.assertContains(detail, f'/static/{product.illustration_path}')
        self.assertContains(response, "Wstrzymaj pokaz")

    def test_category_and_search_can_be_combined(self):
        response = self.client.get(reverse("catalog:list"), {"category": "skis", "q": "TESTOWE"})
        self.assertContains(response, self.product.name)
        response = self.client.get(reverse("catalog:list"), {"category": "boots", "q": "TESTOWE"})
        self.assertContains(response, "Nie znaleźliśmy sprzętu")
        self.assertNotContains(response, self.product.name)

    def test_zero_stock_is_visible_without_purchase_action(self):
        self.product.sale_stock = 0
        self.product.save()
        self.assertContains(self.client.get(reverse("catalog:list")), "Brak w magazynie")
        self.assertContains(self.client.get(self.product.get_absolute_url()), "Aktualnie brak w magazynie")

    @override_settings(DEBUG=False)
    def test_hidden_and_missing_products_return_404(self):
        for slug in (self.hidden.slug, "nie-istnieje"):
            response = self.client.get(reverse("catalog:detail", kwargs={"slug": slug}))
            self.assertEqual(response.status_code, 404)
            self.assertContains(response, "Ta trasa nie istnieje", status_code=404)

    def test_product_description_is_escaped(self):
        self.product.description = '<script>alert("test")</script>'
        self.product.save()
        response = self.client.get(self.product.get_absolute_url())
        self.assertNotContains(response, '<script>alert("test")</script>')
        self.assertContains(response, "&lt;script&gt;")

    def test_invalid_price_and_stock_are_rejected_by_validation(self):
        for field, value in (("price", Decimal("-1")), ("sale_stock", -1)):
            with self.subTest(field=field):
                product = Product(name="Błędny", slug="bledny", category="skis",
                                  description="Test", price="10", sale_stock=1)
                setattr(product, field, value)
                with self.assertRaises(ValidationError):
                    product.full_clean()

    def test_database_protects_price_stock_and_unique_slug(self):
        for values in ({"price": "-1"}, {"sale_stock": -1}):
            with self.subTest(values=values), self.assertRaises(IntegrityError), transaction.atomic():
                Product.objects.filter(pk=self.product.pk).update(**values)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(name="Duplikat", slug=self.product.slug,
                                   category="skis", description="Test", price="10")

    def test_demo_command_is_repeatable_and_preserves_edits(self):
        output = StringIO()
        call_command("seed_demo", stdout=output)
        product = Product.objects.get(slug="narty-alpine-172")
        product.price = Decimal("888.00")
        product.save()
        count = Product.objects.count()
        call_command("seed_demo", stdout=output)
        product.refresh_from_db()
        self.assertEqual(Product.objects.count(), count)
        self.assertEqual(product.price, Decimal("888.00"))


class AdminTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Narty", slug="narty", category="skis",
                                              description="Test", price="100", sale_stock=1)
        self.edit_url = reverse("admin:catalog_product_change", args=[self.product.pk])

    def test_anonymous_and_customer_cannot_edit(self):
        for logged_in in (False, True):
            if logged_in:
                user = get_user_model().objects.create_user(username="klient")
                self.client.force_login(user)
            response = self.client.post(self.edit_url, {"price": "1", "sale_stock": 100})
            self.assertEqual(response.status_code, 302)
            self.assertIn("/admin/login/", response.url)
            self.product.refresh_from_db()
            self.assertEqual(self.product.sale_stock, 1)

    def test_admin_edit_is_reflected_in_public_catalog(self):
        user = get_user_model().objects.create_superuser(username="administrator")
        self.client.force_login(user)
        response = self.client.post(self.edit_url, {
            "name": self.product.name, "slug": self.product.slug, "category": "skis",
            "description": "Zmieniono w panelu", "price": "789.50", "sale_stock": 6,
            "is_active": "on", "_save": "Zapisz",
        })
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        response = self.client.get(reverse("catalog:list"))
        self.assertContains(response, "789,50 zł")
        self.assertContains(response, "Dostępne: 6 szt.")
