from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.demo_data import load_demo_catalogue
from catalog.models import Material, Product

TRANSLATION_FIELDS = ("description_en", "construction_en", "dimensions_en", "weight_scope_en", "size_en")

SPECIFICATION_FIELDS = ("size", "construction", "dimensions", "weight_g", "weight_scope", "specifications_are_demo")


class Command(BaseCommand):
    help = "Uzupełnia katalog fikcyjnymi ofertami ze zdjęciami i cenami z ofert referencyjnych."

    def add_arguments(self, parser):
        parser.add_argument("--refresh-translations", action="store_true", help="Odświeża wyłącznie angielskie treści ofert demo i materiałów.")
        parser.add_argument(
            "--refresh-specs", action="store_true",
            help="Odświeża tylko opisy, parametry i materiały ofert demo; zachowuje ceny, zdjęcia, stany i nazwy.",
        )
        parser.add_argument(
            "--refresh-demo", action="store_true",
            help="Odświeża ceny, zdjęcia, opisy, podkategorie, parametry i materiały ofert demo. Zachowuje nazwy, stany i wyróżnienia.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created_count = updated_count = 0
        refresh_fields = ("price", "discount_percent", "image_path", "description", "subcategory", *SPECIFICATION_FIELDS, *TRANSLATION_FIELDS)
        data = load_demo_catalogue()
        materials = {item["code"]: Material.objects.get_or_create(code=item["code"], defaults={"name": item["name"], "name_en": item.get("name_en", "")})[0] for item in data.get("materials", [])}
        if options["refresh_translations"] or options["refresh_demo"]:
            for item in data.get("materials", []):
                material = materials[item["code"]]
                if material.name == item["name"]:
                    material.name_en = item.get("name_en", "")
                    material.save(update_fields=["name_en"])
        for entry in data["products"]:
            values = entry["product"].copy()
            values["price"] = Decimal(values["price"])
            slug = values.pop("slug")
            product, created = Product.objects.get_or_create(slug=slug, defaults=values)
            if created:
                product.full_clean()
                product.materials.set([materials[code] for code in entry.get("materials", [])])
                created_count += 1
                continue
            if not (options["refresh_demo"] or options["refresh_specs"] or options["refresh_translations"]):
                continue
            if product.category != values["category"]:
                self.stdout.write(self.style.WARNING(f"Pominięto ofertę ze zmienioną kategorią: {slug}"))
                continue
            fields = refresh_fields if options["refresh_demo"] else (("description", *SPECIFICATION_FIELDS, *TRANSLATION_FIELDS) if options["refresh_specs"] else TRANSLATION_FIELDS)
            changed = [field for field in fields if getattr(product, field) != values[field]]
            selected_materials = [materials[code] for code in entry.get("materials", [])]
            materials_changed = not (options["refresh_translations"] and not options["refresh_demo"] and not options["refresh_specs"]) and set(product.materials.values_list("pk", flat=True)) != {item.pk for item in selected_materials}
            if changed:
                for field in changed:
                    setattr(product, field, values[field])
                product.full_clean()
                product.save(update_fields=changed)
            if materials_changed:
                product.materials.set(selected_materials)
            if changed or materials_changed:
                updated_count += 1
        self.stdout.write(self.style.SUCCESS(
            f"Dodano produktów: {created_count}. Odświeżono: {updated_count}. "
            "Nazwy, własne stany i ustawienia widoczności istniejących ofert zachowano."
        ))
