from collections import Counter
from decimal import Decimal
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from .demo_data import load_demo_catalogue
from .models import Product
from .taxonomy import SUBCATEGORIES


class DemoCatalogueTests(TestCase):
    def seed(self, **options):
        call_command("seed_demo", stdout=StringIO(), **options)

    def test_catalogue_covers_every_subcategory_with_two_visible_products(self):
        self.seed()
        self.assertEqual(Product.objects.count(), 61)
        counts = Counter(Product.objects.filter(is_active=True).values_list("category", flat=True))
        expected = {category: 2 * len(choices) for category, choices in SUBCATEGORIES.items()}
        expected[Product.Category.ACCESSORIES] = 3
        self.assertEqual(counts, expected)
        for category, choices in SUBCATEGORIES.items():
            for value, label in choices:
                with self.subTest(category=category, subcategory=label):
                    products = Product.objects.filter(category=category, subcategory=value, is_active=True)
                    self.assertEqual(products.count(), 2)
                    self.assertTrue(products.filter(sale_stock__gt=0).exists())
                    response = self.client.get('/katalog/', {'category': category, 'subcategory': value})
                    self.assertEqual(response.status_code, 200)
                    for product in products:
                        self.assertContains(response, product.name)
        for product in Product.objects.all():
            product.full_clean()
            self.assertGreater(product.price, 0)
        self.seed()
        self.assertEqual(Product.objects.count(), 61)

    def test_photos_and_price_references_are_available_without_network(self):
        data = load_demo_catalogue()
        for entry in data["products"]:
            with self.subTest(product=entry["product"]["slug"]):
                product, reference = entry["product"], entry["reference"]
                photo = Path(settings.BASE_DIR) / "static" / product["image_path"]
                self.assertTrue(photo.is_file())
                content = photo.read_bytes()
                self.assertTrue(content.startswith((bytes.fromhex("ffd8"), b'\x89PNG\r\n\x1a\n')))
                self.assertEqual(Decimal(product["price"]), Decimal(reference["price_pln"]))
                self.assertTrue(reference["url"].startswith(("https://www.decathlon.pl/", "https://www.rossignol-outlet.pl/")))
        self.assertEqual(data["checked_on"], "2026-10-31")

    def test_default_seed_preserves_edits_and_refresh_only_updates_explicit_fields(self):
        self.seed()
        product = Product.objects.get(slug="narty-alpine-172")
        product.name = "Moja oferta"
        product.price = Decimal("888.00")
        product.description = "Mój opis"
        product.sale_stock = 42
        product.featured_order = 7
        product.is_active = False
        product.save()
        self.seed()
        product.refresh_from_db()
        self.assertEqual(product.price, Decimal("888.00"))
        self.assertEqual(product.description, "Mój opis")
        self.seed(refresh_demo=True)
        product.refresh_from_db()
        self.assertEqual(product.price, Decimal("1699.00"))
        self.assertNotEqual(product.description, "Mój opis")
        self.assertEqual(product.name, "Moja oferta")
        self.assertEqual(product.sale_stock, 42)
        self.assertEqual(product.featured_order, 7)
        self.assertFalse(product.is_active)
        self.assertEqual(Product.objects.count(), 61)

    def test_refresh_does_not_touch_custom_products_or_reclassified_demo(self):
        self.seed()
        custom = Product.objects.create(name="Własny produkt", slug="wlasny-produkt", category="accessories", price="17.50")
        product = Product.objects.get(slug="snowboard-drift-156")
        product.category = "accessories"
        product.subcategory = ""
        product.price = Decimal("91.00")
        product.save()
        self.seed(refresh_demo=True)
        custom.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(custom.price, Decimal("17.50"))
        self.assertEqual(product.category, "accessories")
        self.assertEqual(product.price, Decimal("91.00"))
