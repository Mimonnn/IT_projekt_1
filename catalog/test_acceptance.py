"""Próba prezentacji przez prawdziwe HTTP, cookies i CSRF, na osobnej bazie testowej."""
from datetime import timedelta
from decimal import Decimal
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from io import StringIO
import secrets
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import LiveServerTestCase
from django.utils import timezone

from accounts.models import CartItem, Favorite
from orders.models import Order
from rentals.models import RentalItem, Reservation
from .models import Product


class Inputs(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.values = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("name"):
            self.values[attrs["name"]] = attrs.get("value", "")


class BrowserSession:
    def __init__(self, base, language):
        self.base, self.language = base, language
        self.cookies = CookieJar()
        self.opener = build_opener(HTTPCookieProcessor(self.cookies))

    def request(self, path, data=None, csrf=True):
        headers = {"Accept-Language": self.language, "Referer": self.base+"/"}
        if data is not None:
            data = dict(data)
            if csrf:
                data["csrfmiddlewaretoken"] = next(cookie.value for cookie in self.cookies if cookie.name == "csrftoken")
        request = Request(self.base+path, data=urlencode(data).encode() if data is not None else None, headers=headers)
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as error:
            response = error
        with response:
            return response.status, response.read().decode("utf-8"), response.geturl()


class PresentationAcceptanceTests(LiveServerTestCase):
    # Jawny IPv4: nie czekamy na niedostępne lokalne połączenie IPv6 w Windows.
    host = "127.0.0.1"

    def setUp(self):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_rental_demo", stdout=StringIO())

    def exercise(self, language):
        client = BrowserSession(self.live_server_url, language)
        def get(path):
            status, html, _ = client.request(path)
            self.assertEqual(status, 200, path)
            return html
        def post(path, data):
            status, html, url = client.request(path, data)
            self.assertEqual(status, 200, path)
            return html, url
        password = secrets.token_urlsafe(30)
        get("/zarejestruj/")
        post("/zarejestruj/", {"username": "presentation-"+language, "password1": password, "password2": password, "is_staff": "true"})
        user = get_user_model().objects.get(username="presentation-"+language)
        self.assertFalse(user.is_staff)
        post("/konto/dane/", {"first_name": "Anna", "last_name": "Testowa", "email": "presentation@example.com", "phone": "500600700", "is_superuser": "true"})
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Anna")
        self.assertFalse(user.is_superuser)
        product = Product.objects.get(slug="narty-alpine-172")
        original_stock = product.sale_stock
        get("/trasy/beginner/?category=skis")
        get(product.get_absolute_url())
        post(f"/konto/ulubione/dodaj/{product.slug}/", {})
        self.assertTrue(Favorite.objects.filter(user=user, product=product).exists())
        self.assertIn(product.name, get("/konto/ulubione/"))
        csrf_status = client.request(f"/konto/koszyk/dodaj/{product.slug}/", {"quantity": "1"}, csrf=False)[0]
        self.assertEqual(csrf_status, 403)
        admin_password = secrets.token_urlsafe(30)
        get_user_model().objects.create_superuser(username="presentation-staff-"+language, password=admin_password)
        admin = BrowserSession(self.live_server_url, language)
        self.assertEqual(admin.request("/zaloguj/")[0], 200)
        self.assertEqual(admin.request("/zaloguj/", {"username": "presentation-staff-"+language, "password": admin_password})[0], 200)
        def action(path, name, pk):
            self.assertEqual(admin.request(path)[0], 200)
            self.assertEqual(admin.request(path, {"action": name, "_selected_action": pk})[0], 200)
        for method in ("pickup", "courier"):
            post(f"/konto/koszyk/dodaj/{product.slug}/", {"quantity": "1"})
            self.assertIn(product.name, get("/konto/koszyk/"))
            quote = Inputs(get("/zamowienie/")).values["quote"]
            payload = {"quote": quote, "first_name": "Anna", "last_name": "Testowa", "email": "presentation@example.com", "phone": "500600700", "delivery_method": method, "pickup_location": "gliwice", "street_address": "Testowa 1", "postal_code": "44-100", "city": "Gliwice", "accept_demo": "on"}
            _, confirmation = post("/zamowienie/", payload)
            order = Order.objects.filter(user=user).latest("pk")
            self.assertIn(str(order.reference), confirmation)
            self.assertEqual(order.total, product.selling_price+(Decimal("19.99") if method == "courier" else Decimal("0")))
            self.assertFalse(CartItem.objects.filter(user=user).exists())
            self.assertIn(order.number, get("/konto/zamowienia/"))
            for name in ("prepare_selected", "ready_selected" if method == "pickup" else "ship_selected", "complete_selected"):
                action("/admin/orders/order/", name, order.pk)
            order.refresh_from_db()
            self.assertEqual(order.status, "completed")
            self.assertIn(order.number, get("/konto/historia/"))
        product.refresh_from_db()
        self.assertEqual(product.sale_stock, original_stock-2)
        item = RentalItem.objects.get(inventory_code="SZ-N-001")
        dates = {"start_date": timezone.localdate().isoformat(), "end_date": (timezone.localdate()+timedelta(days=2)).isoformat()}
        get("/wypozyczalnia/?"+urlencode({"category": "skis", "model": product.slug, "size": item.size, **dates}))
        get(f"/wypozyczalnia/{item.pk}/?"+urlencode(dates))
        get(f"/wypozyczalnia/{item.pk}/rezerwuj/?"+urlencode(dates))
        post(f"/wypozyczalnia/{item.pk}/rezerwuj/", dates | {"quoted_rate": str(item.daily_rate)})
        reservation = Reservation.objects.get(user=user)
        self.assertEqual(reservation.total_price, item.daily_rate*3)
        self.assertIn(product.name, get("/konto/zamowienia/"))
        self.assertIn(product.name, get("/konto/wypozyczenia/"))
        for name, expected in (("issue_selected", "issued"), ("return_to_service_selected", "returned")):
            action("/admin/rentals/reservation/", name, reservation.pk)
            reservation.refresh_from_db()
            self.assertEqual(reservation.status, expected)
        item.refresh_from_db()
        self.assertEqual(item.status, "service")
        self.assertTrue(reservation.returned_to_service)
        get("/konto/historia/")
        post("/wyloguj/", {})
        get("/zaloguj/")
        post("/zaloguj/", {"username": user.username, "password": password})
        history = get("/konto/historia/")
        self.assertIn(order.number, history)
        self.assertIn(product.name, history)
        outsider = BrowserSession(self.live_server_url, language)
        outsider.request("/zarejestruj/")
        outsider.request("/zarejestruj/", {"username": "outsider-"+language, "password1": password, "password2": password})
        self.assertEqual(outsider.request(order.get_absolute_url())[0], 404)
        self.assertNotIn(order.number, outsider.request("/konto/zamowienia/")[1])
        print(language+": prawdziwe HTTP: rejestracja, profil, ulubione, CSRF, odbiór i kurier, realizacja, rezerwacja, wydanie, zwrot do serwisu, ponowne logowanie i prywatność OK")

    def test_polish_presentation_over_real_http(self):
        self.exercise("pl")

    def test_english_presentation_over_real_http(self):
        self.exercise("en")
