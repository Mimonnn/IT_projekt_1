from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .demo_data import load_demo_catalogue
from .models import Material, Product


class SpecificationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wood = Material.objects.create(code="wood", name="Drewno")
        cls.glass = Material.objects.create(code="fiberglass", name="Włókno szklane")
        cls.steel = Material.objects.create(code="steel", name="Stal")
        cls.first = Product.objects.create(name="Narty Spec 172", slug="spec-172", category="skis", subcategory="downhill", description="Narty do jazdy na trasie.", price="500", size="172 cm", construction="Drewniany rdzeń i laminat.", dimensions="172 × 12 cm", weight_g=4000, weight_scope="para nart z wiązaniami", specifications_are_demo=True)
        cls.first.materials.set([cls.wood, cls.glass])
        cls.second = Product.objects.create(name="Narty Spec 178", slug="spec-178", category="skis", subcategory="freeride", description="Narty w teren.", price="700", size="178 cm")
        cls.second.materials.set([cls.wood, cls.steel])
        cls.hidden = Product.objects.create(name="Ukryty", slug="hidden-spec", category="accessories", size="Rozmiar ukryty", price="1", is_active=False)
        hidden_material = Material.objects.create(code="hidden", name="Materiał ukryty")
        cls.hidden.materials.add(hidden_material)

    def test_filters_combine_category_subcategory_size_material_and_query(self):
        response = self.client.get(reverse("catalog:list"), {"category": "skis", "subcategory": "downhill", "q": "Spec", "size": "172 cm", "material": "wood"})
        self.assertEqual(list(response.context["products"]), [self.first])
        self.assertContains(response, 'value="172 cm" selected')
        self.assertContains(response, 'value="wood" selected')
        self.assertNotContains(response, self.second.name)
        response = self.client.get(reverse("catalog:list"), {"material": "wood"})
        self.assertEqual(set(response.context["products"]), {self.first, self.second})
        response = self.client.get(reverse("catalog:list"), {"material": "fiberglass"})
        self.assertEqual(list(response.context["products"]), [self.first])

    def test_options_are_scoped_and_do_not_leak_hidden_products(self):
        response = self.client.get(reverse("catalog:list"), {"category": "skis", "subcategory": "downhill"})
        self.assertEqual(response.context["sizes"], ["172 cm"])
        self.assertEqual(set(response.context["material_codes"]), {"wood", "fiberglass"})
        self.assertNotContains(response, "Rozmiar ukryty")
        self.assertNotContains(response, "Materiał ukryty")

    def test_unknown_and_incompatible_filters_return_empty_without_losing_selection(self):
        for filters in ({"size": "999 cm"}, {"material": "unknown"}, {"size": "172 cm", "material": "steel"}):
            response = self.client.get(reverse("catalog:list"), filters)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(list(response.context["products"]), [])
            for value in filters.values():
                self.assertContains(response, f'value="{value}" selected')

    def test_detail_shows_material_components_units_and_demo_notice(self):
        response = self.client.get(self.first.get_absolute_url())
        for expected in ("Parametry produktu", "172 cm", "Drewno", "Włókno szklane", "Drewniany rdzeń", "172 × 12 cm", "4000 g", "para nart z wiązaniami", "Parametry demonstracyjne"):
            self.assertContains(response, expected)
        self.assertNotContains(self.client.get(self.second.get_absolute_url()), "Parametry demonstracyjne")

    def test_weight_is_optional_and_must_be_positive(self):
        self.second.full_clean()
        for weight in (0, -1):
            self.second.weight_g = weight
            with self.assertRaises(ValidationError):
                self.second.full_clean()
            with self.assertRaises(IntegrityError), transaction.atomic():
                Product.objects.filter(pk=self.second.pk).update(weight_g=weight)

    def test_admin_can_edit_specifications_and_multiple_materials(self):
        user = get_user_model().objects.create_superuser(username="spec-admin")
        self.client.force_login(user)
        response = self.client.post(reverse("admin:catalog_product_change", args=[self.first.pk]), {
            "name": self.first.name, "slug": self.first.slug, "category": "skis", "subcategory": "downhill", "description": "Nowy opis", "price": "500", "sale_stock": "4", "is_active": "on", "size": "180 cm", "dimensions": "180 × 13 cm", "weight_g": "4200", "weight_scope": "para", "construction": "Własna konstrukcja", "materials": [self.wood.pk, self.steel.pk], "_save": "Zapisz",
        })
        self.assertEqual(response.status_code, 302)
        self.first.refresh_from_db()
        self.assertEqual(self.first.weight_g, 4200)
        self.assertEqual(set(self.first.materials.all()), {self.wood, self.steel})
        self.assertFalse(self.first.specifications_are_demo)
        self.assertContains(self.client.get(self.first.get_absolute_url()), "180 × 13 cm")


class DemoSpecificationTests(TestCase):
    def seed(self, **options):
        call_command("seed_demo", stdout=StringIO(), **options)

    def test_all_61_demo_products_have_full_specifications_and_materials(self):
        self.seed()
        data = load_demo_catalogue()
        self.assertEqual(Product.objects.count(), 61)
        self.assertEqual(Material.objects.count(), len(data["materials"]))
        for product in Product.objects.prefetch_related("materials"):
            with self.subTest(slug=product.slug):
                self.assertTrue(all((product.size, product.dimensions, product.construction, product.weight_g, product.weight_scope)))
                self.assertTrue(product.specifications_are_demo)
                self.assertTrue(product.materials.exists())
                self.assertGreater(len(product.description), 200)
                product.full_clean()

    def test_specs_refresh_preserves_prices_names_stocks_and_images(self):
        self.seed()
        product = Product.objects.get(slug="narty-alpine-172")
        product.name="Nazwa własna"
        product.price=Decimal("123.45")
        product.sale_stock=12
        product.image_path="img/own.jpg"
        product.size="Własny rozmiar"
        product.description="Własny opis"
        product.save()
        product.materials.clear()
        self.seed()
        product.refresh_from_db()
        self.assertEqual(product.size,"Własny rozmiar")
        self.assertFalse(product.materials.exists())
        self.seed(refresh_specs=True)
        product.refresh_from_db()
        self.assertEqual(product.size,"172 cm")
        self.assertNotEqual(product.description,"Własny opis")
        self.assertTrue(product.materials.exists())
        self.assertEqual(product.name,"Nazwa własna")
        self.assertEqual(product.price,Decimal("123.45"))
        self.assertEqual(product.sale_stock,12)
        self.assertEqual(product.image_path,"img/own.jpg")
        self.assertEqual(Product.objects.count(),61)

    def test_specs_refresh_skips_custom_and_reclassified_products(self):
        self.seed()
        custom=Product.objects.create(name="Własny",slug="custom-spec",category="accessories",price="10",size="Własny")
        product=Product.objects.get(slug="narty-alpine-172")
        product.category="accessories"
        product.subcategory=""
        product.size="Bez zmian"
        product.save()
        product.materials.clear()
        self.seed(refresh_specs=True)
        product.refresh_from_db()
        custom.refresh_from_db()
        self.assertEqual(product.size,"Bez zmian")
        self.assertFalse(product.materials.exists())
        self.assertEqual(custom.size,"Własny")
