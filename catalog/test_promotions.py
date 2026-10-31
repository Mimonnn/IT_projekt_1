from decimal import Decimal
from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from accounts.models import CartItem, User
from .models import Product
from .forms import ProductAdminForm


class PromotionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(name="Promocyjne narty", slug="promocyjne-narty", category="skis", subcategory="downhill", description="Opis", price="1699.00", sale_stock=5, discount_percent=10)

    def test_prices_use_decimal_and_round_each_unit_before_quantity(self):
        self.assertEqual(self.product.selling_price, Decimal("1529.10"))
        self.assertEqual(self.product.savings, Decimal("169.90"))
        self.product.price = Decimal("249.99")
        self.product.discount_percent = 15
        self.assertEqual(self.product.selling_price, Decimal("212.49"))
        self.product.price = Decimal("589.99")
        self.product.discount_percent = 20
        self.assertEqual(self.product.selling_price, Decimal("471.99"))
        self.product.price = Decimal("0.05")
        self.product.discount_percent = 10
        self.assertEqual(self.product.selling_price, Decimal("0.05"))

    def test_discount_validation_in_model_and_database(self):
        for discount in (-1, 100):
            self.product.discount_percent = discount
            with self.assertRaises(ValidationError):
                self.product.full_clean()
            with self.assertRaises(IntegrityError), transaction.atomic():
                Product.objects.filter(pk=self.product.pk).update(discount_percent=discount)

    def test_home_promotions_are_independent_of_featured_section(self):
        response = self.client.get(reverse("catalog:home"))
        self.assertContains(response, 'id="promotions-title"')
        self.assertContains(response, "1529,10 zł")
        self.assertContains(response, "1699,00 zł")
        self.assertContains(response, "−10%")
        self.assertEqual(list(response.context["promotion_products"]), [self.product])
        self.assertFalse(response.context["featured_products"])

    def test_hidden_out_of_stock_and_regular_products_are_not_promoted(self):
        for slug, discount, active, stock in [("hidden-promo", 15, False, 3), ("sold-out-promo", 20, True, 0), ("regular", 0, True, 4)]:
            Product.objects.create(name=slug, slug=slug, category="accessories", price="100", discount_percent=discount, is_active=active, sale_stock=stock)
        response = self.client.get(reverse("catalog:home"))
        self.assertEqual(list(response.context["promotion_products"]), [self.product])
        self.product.discount_percent = 0
        self.product.save()
        self.assertNotContains(self.client.get(reverse("catalog:home")), 'id="promotions-title"')

    def test_catalog_detail_and_cart_use_same_discounted_price(self):
        for url in (reverse("catalog:list"), self.product.get_absolute_url()):
            self.assertContains(self.client.get(url), "1529,10 zł")
        user = User.objects.create_user(username="promo-client")
        item = CartItem.objects.create(user=user, product=self.product, quantity=3)
        self.assertEqual(item.subtotal, Decimal("4587.30"))
        self.client.force_login(user)
        response = self.client.get(reverse("accounts:cart"))
        self.assertEqual(response.context["total"], Decimal("4587.30"))
        self.assertContains(response, "1529,10 zł / szt.")
        self.product.discount_percent = 0
        self.product.save()
        self.assertEqual(self.client.get(reverse("accounts:cart")).context["total"], Decimal("5097.00"))

    def test_seed_defines_three_promotions_and_preserves_existing_discount(self):
        call_command("seed_demo", stdout=StringIO())
        expected = {"narty-alpine-172":10, "gogle-halo-s3":15, "buty-snowboardowe-roam-500":20}
        for slug, discount in expected.items():
            self.assertEqual(Product.objects.get(slug=slug).discount_percent, discount)
        product = Product.objects.get(slug="narty-alpine-172")
        product.discount_percent = 7
        product.save()
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_demo", refresh_specs=True, stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual(product.discount_percent, 7)
        call_command("seed_demo", refresh_demo=True, stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual(product.discount_percent, 10)

    def test_home_shows_at_most_three_offers(self):
        for index in range(4):
            Product.objects.create(name=f"Promo {index}", slug=f"promo-{index}", category="accessories", price="100", sale_stock=3, discount_percent=20)
        self.assertEqual(len(self.client.get(reverse("catalog:home")).context["promotion_products"]), 3)

    def test_admin_preserves_missing_discount_and_allows_explicit_clearing(self):
        values = {"name": self.product.name, "slug": self.product.slug, "category": "skis", "subcategory": "downhill", "description": "Opis", "price": "1699.00", "sale_stock": "5"}
        form = ProductAdminForm(values, instance=self.product)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["discount_percent"], 10)
        form = ProductAdminForm({**values, "discount_percent": ""}, instance=self.product)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["discount_percent"], 0)
