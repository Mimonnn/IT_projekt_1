import secrets
from datetime import timedelta
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from catalog.models import Product
from rentals.models import RentalItem, Reservation


class RentalWalkthrough(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_demo', stdout=StringIO())
        call_command('seed_rental_demo', stdout=StringIO())

    def exercise(self, language):
        accounts = []
        for username, staff in [('walk-client-a', False), ('walk-client-b', False), ('walk-admin', True)]:
            password = secrets.token_urlsafe(30)
            user = get_user_model().objects.create_user(username=username, password=password, is_staff=staff, is_superuser=staff)
            client = Client(enforce_csrf_checks=True)
            client.cookies['django_language'] = language
            client.get(reverse('accounts:login'))
            response = client.post(reverse('accounts:login'), {'username': username, 'password': password, 'csrfmiddlewaretoken': client.cookies['csrftoken'].value})
            self.assertEqual(response.status_code, 302)
            accounts.append((user, client))
        (customer_a, a), (customer_b, b), (employee, admin) = accounts
        item = RentalItem.objects.get(inventory_code='SZ-N-001')
        before = list(Product.objects.order_by('pk').values_list('pk', 'sale_stock', 'price', 'discount_percent'))
        today = timezone.localdate()
        dates = {'start_date': today.isoformat(), 'end_date': (today+timedelta(days=2)).isoformat()}
        filters = {'category': 'skis', 'model': item.product.slug, 'size': item.size, **dates}
        list_url = reverse('rentals:list')
        reserve_url = reverse('rentals:reserve', args=[item.pk])
        mine = reverse('rentals:mine')
        admin_url = reverse('admin:rentals_reservation_changelist')

        def post(client, url, data=None):
            return client.post(url, {**(data or {}), 'csrfmiddlewaretoken': client.cookies['csrftoken'].value})

        def action(name, reservation):
            admin.get(admin_url)
            self.assertEqual(post(admin, admin_url, {'action': name, '_selected_action': [reservation.pk]}).status_code, 302)
            reservation.refresh_from_db()
            item.refresh_from_db()

        def confirm(client, selected_dates):
            preview = client.get(reserve_url, selected_dates)
            self.assertTrue(preview.context['available'])
            self.assertEqual(post(client, reserve_url, {**selected_dates, 'quoted_rate': '65.00'}).status_code, 302)
            return Reservation.objects.latest('pk')

        response = a.get(list_url, filters)
        self.assertIn(item.pk, [row.pk for row in response.context['items']])
        detail = a.get(reverse('rentals:detail', args=[item.pk]), filters)
        self.assertEqual(detail.context['total'], Decimal('195.00'))
        self.assertContains(detail, 'Materials' if language == 'en' else 'Materiały')
        reservation = confirm(a, dates)
        self.assertEqual(reservation.user, customer_a)
        self.assertEqual(reservation.total_price, Decimal('195.00'))
        self.assertContains(a.get(mine), 'Alpine 172')
        self.assertNotContains(b.get(mine), 'Alpine 172')
        self.assertNotIn(item.pk, [row.pk for row in b.get(list_url, filters).context['items']])
        self.assertFalse(b.get(reserve_url, dates).context['available'])
        self.assertEqual(post(b, reserve_url, {**dates, 'quoted_rate': '65.00'}).status_code, 200)
        self.assertEqual(Reservation.objects.count(), 1)
        print(language+': logowanie dwóch klientów i administratora, filtry, szczegóły, cena i blokada drugiej rezerwacji OK')

        action('issue_selected', reservation)
        self.assertEqual(reservation.status, 'issued')
        self.assertEqual(item.status, 'rented')
        self.assertEqual(reservation.issued_by, employee)
        self.assertIsNotNone(reservation.issued_at)
        self.assertContains(a.get(mine), 'Issued' if language == 'en' else 'Wydano')
        post(a, reverse('rentals:cancel', args=[reservation.pk]))
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'issued')
        future_dates = {'start_date': (today+timedelta(days=10)).isoformat(), 'end_date': (today+timedelta(days=11)).isoformat()}
        self.assertNotIn(item.pk, [row.pk for row in b.get(list_url, future_dates).context['items']])
        action('return_selected', reservation)
        self.assertEqual(reservation.status, 'returned')
        self.assertEqual(item.status, 'available')
        self.assertEqual(reservation.returned_by, employee)
        self.assertGreaterEqual(reservation.returned_at, reservation.issued_at)
        self.assertContains(a.get(mine), 'Returned' if language == 'en' else 'Zwrócono')
        print(language+': wydanie, ochrona przed anulowaniem, blokada niezwróconego sprzętu, zwrot na stan i historia klienta OK')

        second = confirm(a, dates)
        action('issue_selected', second)
        action('return_to_service_selected', second)
        self.assertEqual(second.status, 'returned')
        self.assertTrue(second.returned_to_service)
        self.assertEqual(item.status, 'service')
        self.assertFalse(b.get(reverse('rentals:detail', args=[item.pk]), dates).context['available'])
        # Zakończenie serwisu przez rzeczywisty formularz administratora.
        edit_url = reverse('admin:rentals_rentalitem_change', args=[item.pk])
        admin.get(edit_url)
        response = post(admin, edit_url, {'product': item.product_id, 'inventory_code': item.inventory_code,
            'size': item.size, 'size_en': item.size_en, 'daily_rate': '65.00', 'status': 'available', 'is_active': 'on', 'technical_notes': ''})
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, 'available')
        third = confirm(a, future_dates)
        self.assertEqual(post(a, reverse('rentals:cancel', args=[third.pk])).status_code, 302)
        third.refresh_from_db()
        self.assertEqual(third.status, 'cancelled')
        fourth = confirm(b, future_dates)
        self.assertEqual(fourth.user, customer_b)
        self.assertEqual(post(a, reverse('rentals:cancel', args=[fourth.pk])).status_code, 404)
        action('issue_selected', fourth)
        self.assertEqual(fourth.status, 'confirmed')
        action('return_selected', fourth)
        self.assertEqual(fourth.status, 'confirmed')
        self.assertTrue(a.get(list_url, {'start_date': 'wrong'}).context['date_form'].errors)
        self.assertEqual(list(Product.objects.order_by('pk').values_list('pk', 'sale_stock', 'price', 'discount_percent')), before)
        print(language+': zwrot do serwisu, przywrócenie przez formularz, anulowanie i zwolnienie terminu, prywatność, błędne daty/akcje oraz magazyn sklepu OK')

    def test_full_polish_workflow(self):
        self.exercise('pl')

    def test_full_english_workflow(self):
        self.exercise('en')
