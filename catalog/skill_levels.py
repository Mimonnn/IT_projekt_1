"""Treści poradnika; przypisania konkretnych produktów przechowuje baza danych."""
from django.utils.translation import gettext_lazy as _

LEVEL_GUIDES = {
    "beginner": {
        "label": _("Początkujący"),
        "headline": _("Pierwsze skręty, wielka przyjemność"),
        "summary": _("Uczysz się hamowania i skrętów albo wracasz na stok po dłuższej przerwie."),
        "abilities": _("Ćwiczysz kontrolę prędkości, zatrzymywanie się i łączenie pierwszych skrętów. Wybierasz łagodne, przygotowane trasy i spokojne tempo, najlepiej podczas zajęć z instruktorem."),
        "equipment": _("Szukaj łatwego w prowadzeniu sprzętu: nart trasowych, przewidywalnej deski all-mountain i wygodnych butów o łagodniejszym charakterze. W naszym katalogu to między innymi Alpine, Drift, Cloud i Flex. Kask i gogle dobierz do obwodu głowy, dopasowania i warunków światła."),
    },
    "intermediate": {
        "label": _("Średniozaawansowany"),
        "headline": _("Więcej pewności w każdym skręcie"),
        "summary": _("Samodzielnie kontrolujesz prędkość i łączysz skręty na przygotowanych trasach."),
        "abilities": _("Pewnie hamujesz i zmieniasz kierunek. Doskonalisz pracę na krawędziach i dostosowujesz skręty do nachylenia stoku. Chcesz rozwijać technikę lub rozpocząć naukę freestyle w odpowiednio dobranym miejscu."),
        "equipment": _("Sprawdź narty i deski all-mountain, a do nauki freestyle modele twin-tip oraz deski freestyle. Traverse, Drift, Pulse i Orbit to przykłady z naszego katalogu. Buty powinny dawać podparcie odpowiednie do Twojej techniki; modele Roam i Contour rozwijają tę część wyboru."),
    },
    "advanced": {
        "label": _("Zaawansowany"),
        "headline": _("Precyzja dopasowana do Twojego stylu"),
        "summary": _("Świadomie pracujesz na krawędziach i szukasz sprzętu do wybranej dyscypliny."),
        "abilities": _("Panujesz nad tempem i torem jazdy na wymagających trasach. Szukasz precyzji w carvingu, rozwijasz freestyle lub masz doświadczenie i przygotowanie do konkretnej formy jazdy terenowej."),
        "equipment": _("Dobieraj sprzęt do zastosowania: Velocity i Race Pro do sportowej jazdy na trasie, Edge do carvingu, Powder, Glacier i Rift do freeride, a Ascend i Climb do skituringu. To różne dyscypliny: umiejętności na stoku nie zastępują przygotowania terenowego ani lawinowego."),
    },
}
