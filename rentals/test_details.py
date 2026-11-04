from datetime import timedelta
from decimal import Decimal
from io import StringIO
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

from .models import RentalItem, Reservation
from .services import reserve_item


class RentalDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_rental_demo", stdout=StringIO())
        cls.item = RentalItem.objects.select_related("product").get(inventory_code="SZ-N-001")

    def setUp(self):
        self.start = timezone.localdate()+timedelta(days=10)
        self.end = self.start+timedelta(days=2)
        self.dates = {"start_date": self.start.isoformat(), "end_date": self.end.isoformat()}
        self.url = reverse("rentals:detail", args=[self.item.pk])

    def test_anonymous_customer_can_read_specs_without_purchase_actions_or_private_notes(self):
        RentalItem.objects.filter(pk=self.item.pk).update(technical_notes="PRIVATE-DETAIL-NOTE")
        response = self.client.get(self.url)
        for text in ("Alpine 172", "65,00 zł", "Materiały", "Konstrukcja", "Wymiary", "Masa", "Rozmiar egzemplarza", "Parametry modelu", "Parametry demonstracyjne"):
            self.assertContains(response, text)
        for paragraph in self.item.product.display_description.split("\n\n"):
            self.assertContains(response, paragraph)
        self.assertContains(response, reverse("rentals:reserve", args=[self.item.pk]))
        self.assertNotContains(response, "PRIVATE-DETAIL-NOTE")
        self.assertNotContains(response, "Dodaj do koszyka")
        self.assertNotContains(response, "1529,10")

    def test_list_keeps_reserve_action_and_links_photo_name_and_details_with_dates(self):
        filters = {"category": "skis", "model": self.item.product.slug, "size": self.item.size, **self.dates}
        response = self.client.get(reverse("rentals:list"), filters)
        details_link = escape(self.url+"?"+urlencode(filters))
        self.assertContains(response, f'href="{details_link}"', count=3)
        reserve_link = escape(reverse("rentals:reserve", args=[self.item.pk])+"?"+urlencode(self.dates))
        self.assertContains(response, f'href="{reserve_link}"')

    def test_detail_keeps_dates_filters_cost_and_never_creates_reservation_on_get(self):
        filters = {"category": "skis", "model": self.item.product.slug, "size": self.item.size, **self.dates}
        response = self.client.get(self.url, filters)
        self.assertTrue(response.context["available"])
        self.assertEqual(response.context["total"], Decimal("195.00"))
        self.assertEqual(response.context["date_query"], urlencode(self.dates))
        self.assertEqual(response.context["back_query"], urlencode(filters))
        self.assertContains(response, 'name="model" value="narty-alpine-172"')
        reserve_link = escape(reverse("rentals:reserve", args=[self.item.pk])+"?"+urlencode(self.dates))
        self.assertContains(response, f'href="{reserve_link}"')
        self.assertFalse(Reservation.objects.exists())

    def test_hidden_item_or_product_and_missing_item_are_not_public(self):
        RentalItem.objects.filter(pk=self.item.pk).update(is_active=False)
        self.assertEqual(self.client.get(self.url).status_code, 404)
        RentalItem.objects.filter(pk=self.item.pk).update(is_active=True)
        product = self.item.product
        product.is_active = False
        product.save(update_fields=["is_active"])
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.assertEqual(self.client.get(reverse("rentals:detail", args=[99999999])).status_code, 404)

    def test_conflict_service_and_invalid_dates_keep_details_but_prevent_booking(self):
        user = get_user_model().objects.create_user(username="detail-reservation")
        reserve_item(user=user, item_id=self.item.pk, start_date=self.start, end_date=self.end, quoted_rate=Decimal("65.00"))
        for params in (self.dates, {"start_date": "invalid"}):
            response = self.client.get(self.url, params)
            self.assertFalse(response.context["available"])
            self.assertContains(response, "Parametry modelu")
            self.assertNotContains(response, reverse("rentals:reserve", args=[self.item.pk]))
        RentalItem.objects.filter(pk=self.item.pk).update(status="service")
        response = self.client.get(self.url)
        self.assertContains(response, "Do serwisu")
        self.assertNotContains(response, reverse("rentals:reserve", args=[self.item.pk]))

    def test_english_copy_and_item_size_are_used_with_shared_sale_specifications(self):
        RentalItem.objects.filter(pk=self.item.pk).update(size="Rozmiar własny", size_en="Custom size")
        self.client.cookies["django_language"] = "en"
        response = self.client.get(self.url, self.dates)
        for text in ("Model specifications", "Item size", "Custom size", "Materials", "Construction", "Dimensions", "Weight", "195.00 PLN", "Reserve"):
            self.assertContains(response, text)
        for paragraph in self.item.product.description_en.split("\n\n"):
            self.assertContains(response, paragraph)
        response = self.client.get(self.item.product.get_absolute_url())
        self.assertContains(response, "Product specifications")
        self.assertContains(response, "1529.10 PLN")
        self.assertNotContains(response, "Model specifications")
