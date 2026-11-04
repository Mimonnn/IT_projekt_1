from decimal import Decimal

from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from catalog.localization import localized_text


class RentalItem(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", _("Na stanie")
        RENTED = "rented", _("Wypożyczony")
        SERVICE = "service", _("Do serwisu")

    product = models.ForeignKey(
        "catalog.Product", on_delete=models.PROTECT,
        related_name="rental_items", verbose_name=_("model sprzętu"),
    )
    inventory_code = models.CharField(
        _("numer ewidencyjny"), max_length=40, unique=True,
        validators=[RegexValidator(r"\A[A-Z0-9][A-Z0-9-]*\Z", _("Użyj wielkich liter, cyfr i myślników."))],
    )
    size = models.CharField(_("rozmiar"), max_length=80)
    size_en = models.CharField(_("rozmiar (angielski)"), max_length=80, blank=True)
    daily_rate = models.DecimalField(
        _("stawka za dobę (zł)"), max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    status = models.CharField(_("stan egzemplarza"), max_length=12, choices=Status.choices, default=Status.AVAILABLE)
    technical_notes = models.TextField(_("notatki techniczne"), blank=True, help_text=_("Informacje wewnętrzne, niewidoczne dla klientów."))
    is_active = models.BooleanField(_("widoczny w wypożyczalni"), default=True)
    created_at = models.DateTimeField(_("data dodania"), auto_now_add=True)

    class Meta:
        ordering = ["product__name", "inventory_code"]
        verbose_name = _("egzemplarz do wypożyczenia")
        verbose_name_plural = _("egzemplarze do wypożyczenia")
        constraints = [
            models.CheckConstraint(condition=models.Q(daily_rate__gt=0), name="rental_daily_rate_positive"),
            models.CheckConstraint(condition=models.Q(status__in=["available", "rented", "service"]), name="rental_status_valid"),
            models.CheckConstraint(condition=models.Q(inventory_code__regex=r"^[A-Z0-9][A-Z0-9-]*$"), name="rental_inventory_code_valid"),
        ]

    def __str__(self):
        return f"{self.inventory_code} — {self.product.name}"

    @property
    def display_size(self):
        return localized_text(self, "size")


class Reservation(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", _("Zarezerwowano")
        CANCELLED = "cancelled", _("Anulowano")
        ISSUED = "issued", _("Wypożyczony")
        RETURNED = "returned", _("Zwrócono")

    user = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name="rental_reservations", verbose_name=_("klient"))
    item = models.ForeignKey(RentalItem, on_delete=models.PROTECT, related_name="reservations", verbose_name=_("egzemplarz"))
    start_date = models.DateField(_("odbiór"))
    end_date = models.DateField(_("zwrot"))
    daily_rate = models.DecimalField(_("zapisana stawka dobowa (zł)"), max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    product_name = models.CharField(_("zapisana nazwa sprzętu"), max_length=160)
    size = models.CharField(_("zapisany rozmiar"), max_length=80)
    size_en = models.CharField(_("zapisany rozmiar (angielski)"), max_length=80, blank=True)
    status = models.CharField(_("status rezerwacji"), max_length=12, choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(_("data dodania"), auto_now_add=True)
    cancelled_at = models.DateTimeField(_("data anulowania"), null=True, blank=True)

    issued_at = models.DateTimeField(_("data wydania"), null=True, blank=True)
    returned_at = models.DateTimeField(_("data zwrotu sprzętu"), null=True, blank=True)
    issued_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, null=True, blank=True, related_name="issued_rentals", verbose_name=_("sprzęt wydał"))
    returned_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, null=True, blank=True, related_name="received_rentals", verbose_name=_("zwrot przyjął"))
    returned_to_service = models.BooleanField(_("po zwrocie skierowano do serwisu"), default=False)

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("rezerwacja")
        verbose_name_plural = _("rezerwacje")
        constraints = [
            models.CheckConstraint(condition=models.Q(end_date__gte=models.F("start_date")), name="reservation_dates_ordered"),
            models.CheckConstraint(condition=models.Q(daily_rate__gt=0), name="reservation_rate_positive"),
            models.CheckConstraint(condition=models.Q(status__in=["confirmed", "cancelled", "issued", "returned"]), name="reservation_status_valid"),
            models.UniqueConstraint(fields=["item"], condition=models.Q(status="issued"), name="one_issued_rental_per_item"),
            models.CheckConstraint(condition=(
                models.Q(status__in=["confirmed", "cancelled"], issued_at__isnull=True, returned_at__isnull=True, issued_by__isnull=True, returned_by__isnull=True, returned_to_service=False)
                | models.Q(status="issued", issued_at__isnull=False, issued_by__isnull=False, returned_at__isnull=True, returned_by__isnull=True, returned_to_service=False)
                | models.Q(status="returned", issued_at__isnull=False, issued_by__isnull=False, returned_at__isnull=False, returned_by__isnull=False)
            ), name="reservation_handover_consistent"),
            models.CheckConstraint(condition=models.Q(returned_at__isnull=True) | models.Q(returned_at__gte=models.F("issued_at")), name="reservation_return_after_issue"),
        ]

    def __str__(self):
        return f"#{self.pk} — {self.product_name}"

    @property
    def days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_price(self):
        return self.daily_rate * self.days

    @property
    def display_size(self):
        return localized_text(self, "size")

    @property
    def can_customer_cancel(self):
        from django.utils import timezone
        return self.status == self.Status.CONFIRMED and self.start_date >= timezone.localdate()


    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.status == self.Status.ISSUED and self.end_date < timezone.localdate()
