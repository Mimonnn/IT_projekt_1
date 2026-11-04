from django.utils.translation import gettext as _


def interface_strings(request):
    return {"ui_strings": {
        "allSubcategories": _("Wszystkie podkategorie"),
        "allSizes": _("Wszystkie rozmiary"),
        "allMaterials": _("Wszystkie materiały"),
        "notInGroup": _("brak w tej grupie"),
        "pause": _("Wstrzymaj pokaz"),
        "resume": _("Wznów pokaz"),
    }}
