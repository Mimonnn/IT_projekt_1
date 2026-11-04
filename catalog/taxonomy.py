from django.utils.translation import gettext_lazy as _
"""Wspólne definicje podkategorii dla modelu, formularzy i menu."""
from django.db.models import Q, TextChoices


class SkiSubcategory(TextChoices):
    DOWNHILL = "downhill", _("Narty zjazdowe (trasowe)")
    ALL_MOUNTAIN = "all_mountain", _("Narty all-mountain")
    FREERIDE = "freeride", _("Narty freeride")
    FREESTYLE = "freestyle", _("Narty freestyle")
    TOURING = "touring", _("Narty skiturowe")
    CROSS_COUNTRY = "cross_country", _("Narty biegowe")
    RACE = "race", _("Narty sportowe / race")


SUBCATEGORIES = {
    "skis": SkiSubcategory.choices,
    "snowboards": [
        ("all_mountain", _("All-mountain")),
        ("freestyle", _("Freestyle")),
        ("freeride", _("Freeride")),
        ("carving", _("Carvingowe")),
    ],
    "bindings": [
        ("alpine", _("Narciarskie zjazdowe")),
        ("touring", _("Narciarskie skiturowe")),
        ("straps", _("Snowboardowe paskowe")),
        ("quick_entry", _("Snowboardowe z szybkim wpinaniem")),
    ],
    "helmets": [
        ("classic", _("Klasyczne")),
        ("visor", _("Z wizjerem")),
        ("freestyle", _("Freestyle")),
    ],
    "goggles": [
        ("sunny", _("Na słoneczne dni")),
        ("cloudy", _("Na pochmurne dni")),
        ("photochromic", _("Fotochromowe")),
        ("otg", _("OTG")),
    ],
    "snowboard_boots": [
        ("all_mountain", _("All-mountain")),
        ("freestyle", _("Freestyle")),
        ("freeride", _("Freeride")),
    ],
    "boots": [
        ("alpine", _("Zjazdowe / trasowe")),
        ("all_mountain_freeride", _("All-mountain / freeride")),
        ("touring", _("Skiturowe")),
        ("race", _("Sportowe / race")),
    ],
}

ALL_LABELS = {
    "skis": _("Wszystkie narty"),
    "snowboards": _("Wszystkie deski snowboardowe"),
    "bindings": _("Wszystkie wiązania"),
    "helmets": _("Wszystkie kaski"),
    "goggles": _("Wszystkie gogle"),
    "snowboard_boots": _("Wszystkie buty snowboardowe"),
    "boots": _("Wszystkie buty narciarskie"),
}


def subcategory_constraint():
    # Puste wartości zachowują zgodność z produktami sprzed klasyfikacji.
    condition = Q(subcategory="")
    for category, choices in SUBCATEGORIES.items():
        condition |= Q(category=category, subcategory__in=[value for value, _ in choices])
    return condition
