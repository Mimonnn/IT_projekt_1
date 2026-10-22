"""Wspólne definicje podkategorii dla modelu, formularzy i menu."""
from django.db.models import Q, TextChoices


class SkiSubcategory(TextChoices):
    DOWNHILL = "downhill", "Narty zjazdowe (trasowe)"
    ALL_MOUNTAIN = "all_mountain", "Narty all-mountain"
    FREERIDE = "freeride", "Narty freeride"
    FREESTYLE = "freestyle", "Narty freestyle"
    TOURING = "touring", "Narty skiturowe"
    CROSS_COUNTRY = "cross_country", "Narty biegowe"
    RACE = "race", "Narty sportowe / race"


SUBCATEGORIES = {
    "skis": SkiSubcategory.choices,
    "snowboards": [
        ("all_mountain", "All-mountain"),
        ("freestyle", "Freestyle"),
        ("freeride", "Freeride"),
        ("carving", "Carvingowe"),
    ],
    "bindings": [
        ("alpine", "Narciarskie zjazdowe"),
        ("touring", "Narciarskie skiturowe"),
        ("straps", "Snowboardowe paskowe"),
        ("quick_entry", "Snowboardowe z szybkim wpinaniem"),
    ],
    "helmets": [
        ("classic", "Klasyczne"),
        ("visor", "Z wizjerem"),
        ("freestyle", "Freestyle"),
    ],
    "goggles": [
        ("sunny", "Na słoneczne dni"),
        ("cloudy", "Na pochmurne dni"),
        ("photochromic", "Fotochromowe"),
        ("otg", "OTG"),
    ],
    "snowboard_boots": [
        ("all_mountain", "All-mountain"),
        ("freestyle", "Freestyle"),
        ("freeride", "Freeride"),
    ],
    "boots": [
        ("alpine", "Zjazdowe / trasowe"),
        ("all_mountain_freeride", "All-mountain / freeride"),
        ("touring", "Skiturowe"),
        ("race", "Sportowe / race"),
    ],
}

ALL_LABELS = {
    "skis": "Wszystkie narty",
    "snowboards": "Wszystkie deski snowboardowe",
    "bindings": "Wszystkie wiązania",
    "helmets": "Wszystkie kaski",
    "goggles": "Wszystkie gogle",
    "snowboard_boots": "Wszystkie buty snowboardowe",
    "boots": "Wszystkie buty narciarskie",
}


def subcategory_constraint():
    # Puste wartości zachowują zgodność z produktami sprzed klasyfikacji.
    condition = Q(subcategory="")
    for category, choices in SUBCATEGORIES.items():
        condition |= Q(category=category, subcategory__in=[value for value, _ in choices])
    return condition
