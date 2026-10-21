from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Product


class Command(BaseCommand):
    help = "Dodaje fikcyjne produkty demonstracyjne; nie nadpisuje istniejących produktów."

    @transaction.atomic
    def handle(self, *args, **options):
        samples = [
            ("narty-alpine-172", "Alpine 172", "skis", "1299.00", 5,
             "Wszechstronne narty trasowe o długości 172 cm. Model demonstracyjny dla miłośników spokojnych skrętów i całodziennych wypadów na stok."),
            ("buty-summit-27", "Summit 27", "boots", "749.00", 8,
             "Buty narciarskie w rozmiarze mondo 27. Wygodna konstrukcja i cztery klamry. Fikcyjny produkt przygotowany na potrzeby projektu."),
            ("snowboard-drift-156", "Drift 156", "snowboards", "1099.00", 3,
             "Snowboard all-mountain o długości 156 cm. Uniwersalny model demonstracyjny do odkrywania nowych tras."),
            ("kask-ridge-m", "Ridge M", "helmets", "249.00", 0,
             "Lekki kask zimowy w rozmiarze M, z regulacją dopasowania. Fikcyjny model; aktualnie brak sztuk na sprzedaż."),
        ]
        created_count = 0
        featured = {
            "snowboard-drift-156": {"image_path": "img/snowboard1.jpg", "featured_order": 1},
            "narty-alpine-172": {"image_path": "img/narty.jpg", "featured_order": 2},
        }
        for slug, name, category, price, stock, description in samples:
            _, created = Product.objects.get_or_create(slug=slug, defaults={
                "name": name, "category": category, "price": price,
                "sale_stock": stock, "description": description,
                **featured.get(slug, {}),
            })
            created_count += created
        self.stdout.write(self.style.SUCCESS(
            f"Dodano produktów: {created_count}. Istniejące pozostawiono bez zmian."))

