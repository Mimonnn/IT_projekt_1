from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalog.models import Product
from rentals.models import RentalItem


# Stawki i egzemplarze są fikcyjnymi danymi demonstracyjnymi.
DEMO_ITEMS = (
    ("SZ-N-001", "narty-alpine-172", "65.00", RentalItem.Status.AVAILABLE),
    ("SZ-N-002", "narty-alpine-172", "65.00", RentalItem.Status.AVAILABLE),
    ("SZ-N-003", "narty-traverse-84", "75.00", RentalItem.Status.AVAILABLE),
    ("SZ-N-004", "narty-traverse-84", "75.00", RentalItem.Status.SERVICE),
    ("SZ-S-001", "snowboard-drift-156", "60.00", RentalItem.Status.AVAILABLE),
    ("SZ-S-002", "snowboard-drift-156", "60.00", RentalItem.Status.AVAILABLE),
    ("SZ-S-003", "snowboard-orbit-152", "55.00", RentalItem.Status.AVAILABLE),
    ("SZ-S-004", "snowboard-orbit-152", "55.00", RentalItem.Status.AVAILABLE),
    ("SZ-K-001", "kask-ridge-m", "15.00", RentalItem.Status.AVAILABLE),
    ("SZ-K-002", "kask-ridge-m", "15.00", RentalItem.Status.AVAILABLE),
)


class Command(BaseCommand):
    help = "Dodaje egzemplarze demo wypożyczalni, zachowując istniejące edycje i magazyn sprzedaży."

    @transaction.atomic
    def handle(self, *args, **options):
        products = {p.slug: p for p in Product.objects.filter(slug__in={row[1] for row in DEMO_ITEMS})}
        missing = sorted({row[1] for row in DEMO_ITEMS} - products.keys())
        if missing:
            raise CommandError("Najpierw uruchom seed_demo. Brak produktów: " + ", ".join(missing))
        created_count = 0
        for code, slug, rate, status in DEMO_ITEMS:
            product = products[slug]
            _, created = RentalItem.objects.get_or_create(inventory_code=code, defaults={
                "product": product, "size": product.size, "size_en": product.size_en,
                "daily_rate": Decimal(rate), "status": status,
            })
            created_count += created
        self.stdout.write(self.style.SUCCESS(f"Dodano egzemplarze demo: {created_count}. Zachowano istniejące: {len(DEMO_ITEMS) - created_count}."))
