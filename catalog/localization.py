from django.utils.translation import get_language


def localized_text(instance, field):
    """Angielskie dane są opcjonalne; własne nieprzetłumaczone oferty zachowują tekst źródłowy."""
    if (get_language() or "pl").split("-")[0] == "en":
        english = getattr(instance, field + "_en", "")
        if english:
            return english
    return getattr(instance, field)
