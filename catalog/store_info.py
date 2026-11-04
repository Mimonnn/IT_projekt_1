from django.utils.translation import gettext_lazy as _
"""Publiczne, fikcyjne dane demonstracyjne; nie kontaktują z realną firmą."""

SUPPORT = {
    "email": "pomoc@szron.example",
    "phone": "+48 000 000 101",
    "person": _("Marta — doradczyni klienta"),
    "hours": _("Poniedziałek–piątek, 9:00–17:00"),
}

STORES = [
    {"name": _("Szron Gliwice"), "city": "Gliwice", "address": "ul. Zimowego Szlaku 12", "hours": _("Pon.–pt. 10:00–18:00, sob. 10:00–14:00"), "description": _("Salon miejski — sprzęt narciarski i snowboardowy oraz dobór akcesoriów.")},
    {"name": _("Szron Katowice"), "city": "Katowice", "address": "ul. Śnieżnej Grani 8", "hours": _("Pon.–pt. 10:00–19:00, sob. 10:00–15:00"), "description": _("Salon miejski — przymierzanie butów, wybór sprzętu i konsultacje przed wyjazdem.")},
    {"name": _("Szron Szczyrk — przy stoku"), "city": "Szczyrk", "address": "ul. Pod Białym Stokiem 3", "hours": _("W sezonie zimowym: codziennie 8:00–18:00"), "description": _("Fikcyjny punkt przy dolnej stacji stoku — sklep, wypożyczalnia i przygotowanie sprzętu do jazdy.")},
    {"name": _("Szron Białka — przy stoku"), "city": "Białka Tatrzańska", "address": "ul. Narciarskiej Polany 6", "hours": _("W sezonie zimowym: codziennie 8:00–19:00"), "description": _("Fikcyjny punkt obok tras narciarskich — sprzęt na stok, akcesoria i obsługa wypożyczalni.")},
]
