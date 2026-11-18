import importlib
import re
from decimal import Decimal
from io import StringIO
from types import SimpleNamespace

from django.apps import apps
from django.core.management import call_command
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import translation

from accounts.forms import ProfileForm
from accounts.models import User
from .forms import ProductAdminForm
from .models import Material, Product


class BilingualSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", stdout=StringIO())

    def english_client(self):
        client = Client()
        client.cookies["django_language"] = "en"
        return client

    def test_switch_preserves_current_page_and_filters_and_remembers_choice(self):
        target = "/katalog/?category=skis&size=172+cm&material=wood"
        response = self.client.post(reverse("set_language"), {"language": "en", "next": target})
        self.assertRedirects(response, target)
        self.assertEqual(int(response.cookies["django_language"]["max-age"]), 31536000)
        self.assertEqual(self.client.cookies["django_language"].value, "en")
        response = self.client.get(target)
        self.assertContains(response, '<html lang="en">')
        self.assertContains(response, "Products found: 2")
        self.assertContains(response, "All categories")
        self.assertEqual(response.headers["Content-Language"], "en")
        self.client.post(reverse("set_language"), {"language": "pl", "next": target})
        response = self.client.get(target)
        self.assertContains(response, '<html lang="pl">')
        self.assertContains(response, "Znalezione produkty: 2")

    def test_switch_rejects_external_redirect_and_requires_csrf(self):
        response = self.client.post(reverse("set_language"), {"language": "en", "next": "https://example.org/"})
        self.assertEqual(response.url, "/")
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse("set_language"), {"language": "en"}).status_code, 403)
        client.get(reverse("accounts:login"))
        response = client.post(reverse("set_language"), {"language": "en", "csrfmiddlewaretoken": client.cookies["csrftoken"].value})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.cookies["django_language"].value, "en")

    def test_public_pages_render_in_english(self):
        client = self.english_client()
        for name, heading in [("home", "It all starts"), ("list", "Find your equipment."), ("terms", "Szron website terms"), ("contact", "How can we help?"), ("stores", "Meet us before you hit the slopes.")]:
            with self.subTest(page=name):
                response = client.get(reverse("catalog:"+name))
                self.assertContains(response, heading)
                self.assertContains(response, "Sign in")
                self.assertNotContains(response, ">Strona główna<")
        self.assertContains(client.get("/missing-page/"), "This trail does not exist.", status_code=404)

    def test_all_products_have_complete_english_copy_without_changing_polish(self):
        self.assertEqual(Product.objects.count(), 61)
        for product in Product.objects.all():
            with self.subTest(product=product.slug):
                original = product.description
                with translation.override("en"):
                    for field in ("description", "construction", "dimensions", "size", "weight_scope"):
                        text = getattr(product, "display_"+field)
                        self.assertTrue(getattr(product, field+"_en"))
                        self.assertFalse(re.search("[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", text), text)
                    self.assertEqual(product.get_category_display(), {"skis":"Skis","snowboards":"Snowboards","bindings":"Bindings","helmets":"Helmets","goggles":"Goggles","snowboard_boots":"Snowboard boots","boots":"Ski boots","accessories":"Accessories"}[product.category])
                with translation.override("pl"):
                    self.assertEqual(product.display_description, original)

    def test_detail_material_and_size_filters_use_localized_labels_and_stable_values(self):
        client = self.english_client()
        response = client.get("/katalog/narty-alpine-172/")
        for text in ("Product specifications", "Wood", "Demo specifications", "1529.10 PLN", "pair of skis with bindings"):
            self.assertContains(response, text)
        self.assertNotContains(response, "Drewniany rdzeń")
        response = client.get(reverse("catalog:list"), {"category":"accessories", "size":"Do nart do 190 cm", "material":"polyester"})
        self.assertContains(response, "Products found: 1")
        self.assertContains(response, "Skis up to 190 cm")
        self.assertContains(response, 'value="Do nart do 190 cm"')
        self.assertEqual(response.context["ui_strings"]["allSizes"], "All sizes")
        self.assertEqual(response.context["ui_strings"]["resume"], "Resume slideshow")

    def test_account_pages_forms_and_messages_follow_language(self):
        client = self.english_client()
        user = User.objects.create_user(username="bilingual-client")
        client.force_login(user)
        for name, heading in [("orders","Orders and reservations"),("history","Purchase history"),("returns","Returns"),("cart","Your basket"),("favorites","Favourite products"),("edit_profile","Profile details")]:
            response = client.get(reverse("accounts:"+name))
            self.assertContains(response, heading)
        response = client.post(reverse("accounts:cart_add", args=["narty-alpine-172"]), {"quantity":1}, follow=True)
        self.assertContains(response, "Added to basket: Alpine 172.")
        self.assertEqual(response.context["total"], Decimal("1529.10"))
        self.assertContains(response,"1529.10 PLN / item")
        client.post(reverse("accounts:logout"))
        self.assertContains(client.get(reverse("catalog:home")), "Sign in")
        self.assertEqual(client.cookies["django_language"].value,"en")
        with translation.override("en"):
            self.assertEqual(ProfileForm().fields["first_name"].label,"First name")
            form = ProductAdminForm(instance=Product.objects.get(slug="narty-alpine-172"))
            self.assertIn("Alpine piste skis", [str(label) for _, label in form.fields["subcategory"].choices])

    def test_custom_content_falls_back_to_source_when_english_is_missing(self):
        product = Product.objects.create(name="Custom",slug="custom-language",category="accessories",description="Własny opis",price="12")
        with translation.override("en"):
            self.assertEqual(product.display_description,"Własny opis")

    def test_translation_refresh_preserves_prices_polish_data_and_material_selection(self):
        product = Product.objects.get(slug="narty-alpine-172")
        product.price=Decimal("333.33")
        product.description="Własny polski opis"
        product.description_en="My English description"
        product.save()
        product.materials.clear()
        call_command("seed_demo",stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual(product.description_en,"My English description")
        call_command("seed_demo",refresh_translations=True,stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual(product.description,"Własny polski opis")
        self.assertEqual(product.price,Decimal("333.33"))
        self.assertFalse(product.materials.exists())
        self.assertIn("Piste skis",product.description_en)

    def test_backfill_preserves_custom_source_and_existing_english(self):
        product = Product.objects.get(slug="narty-alpine-172")
        product.description="Inny opis źródłowy"
        product.description_en=""
        product.construction_en="Own construction"
        product.dimensions_en=""
        product.save()
        migration=importlib.import_module("catalog.migrations.0013_translate_demo_catalogue")
        migration.populate_english(apps,SimpleNamespace(connection=connection))
        product.refresh_from_db()
        self.assertEqual(product.description_en,"")
        self.assertEqual(product.construction_en,"Own construction")
        self.assertTrue(product.dimensions_en)

    def test_admin_uses_english_and_provides_language_switch(self):
        client = self.english_client()
        user = User.objects.create_superuser(username="bilingual-admin")
        client.force_login(user)
        response = client.get(reverse("admin:index"))
        self.assertContains(response, "Szron — administration")
        self.assertContains(response, 'class="admin-language-switch"')
        response = client.get(reverse("admin:catalog_product_change", args=[Product.objects.get(slug="narty-alpine-172").pk]))
        self.assertContains(response, "Description (English)")
        self.assertContains(response, "Alpine piste skis")


    def test_shop_pages_describe_working_rentals_in_both_languages(self):
        for language, banner, notice, action in (
            ("pl", "Wybierz sprzęt, sprawdź dostępność", "Sprzęt możesz już rezerwować w wypożyczalni.", "Przejdź do wypożyczalni"),
            ("en", "Choose equipment, check availability", "You can already reserve equipment in the rental section.", "Browse rentals"),
        ):
            with self.subTest(language=language):
                self.client.cookies["django_language"] = language
                response = self.client.get(reverse("catalog:home"))
                self.assertContains(response, banner)
                self.assertContains(response, f'<a class="coming-soon" href="/wypozyczalnia/">{action} ↗</a>', html=True)
                response = self.client.get("/katalog/narty-alpine-172/")
                self.assertContains(response, notice)
                self.assertNotContains(response, "Składanie zamówień i rezerwacje udostępnimy")
