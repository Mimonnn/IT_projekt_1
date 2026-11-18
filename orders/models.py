import uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from catalog.store_info import STORES

PICKUP_KEYS = ("gliwice", "katowice", "szczyrk", "bialka")
PICKUP_CHOICES = [(key, store["name"]) for key, store in zip(PICKUP_KEYS, STORES)]
DELIVERY_FEES = {"pickup": Decimal("0.00"), "courier": Decimal("19.99")}


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("Przyjęte")
        PREPARING = "preparing", _("W przygotowaniu")
        READY = "ready", _("Gotowe do odbioru")
        SHIPPED = "shipped", _("Wysłane")
        COMPLETED = "completed", _("Zrealizowane")
        CANCELLED = "cancelled", _("Anulowano")

    class Delivery(models.TextChoices):
        PICKUP = "pickup", _("Odbiór w sklepie")
        COURIER = "courier", _("Kurier za pobraniem")

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    checkout_token = models.UUIDField(unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="purchase_orders", verbose_name=_("klient"))
    status = models.CharField(_("status zamówienia"), max_length=12, choices=Status.choices, default=Status.NEW)
    first_name = models.CharField(_("Imię"), max_length=150)
    last_name = models.CharField(_("Nazwisko"), max_length=150)
    email = models.EmailField(_("Adres e-mail"))
    phone = models.CharField(_("Numer telefonu"), max_length=25)
    delivery_method = models.CharField(_("Sposób dostawy"), max_length=12, choices=Delivery.choices)
    pickup_location = models.CharField(_("Sklep odbioru"), max_length=12, choices=PICKUP_CHOICES, blank=True)
    pickup_address = models.CharField(_("adres sklepu odbioru"), max_length=240, blank=True)
    street_address = models.CharField(_("Ulica i numer domu / mieszkania"), max_length=200, blank=True)
    postal_code = models.CharField(_("Kod pocztowy"), max_length=6, blank=True)
    city = models.CharField(_("Miejscowość"), max_length=100, blank=True)
    notes = models.TextField(_("Uwagi do zamówienia"), max_length=1000, blank=True)
    subtotal = models.DecimalField(_("Wartość produktów"), max_digits=22, decimal_places=2)
    delivery_fee = models.DecimalField(_("Koszt dostawy"), max_digits=10, decimal_places=2)
    total = models.DecimalField(_("Razem"), max_digits=22, decimal_places=2)
    created_at = models.DateTimeField(_("data dodania"), auto_now_add=True)
    updated_at = models.DateTimeField(_("ostatnia zmiana"), auto_now=True)
    completed_at = models.DateTimeField(_("data realizacji"), null=True, blank=True)
    cancelled_at = models.DateTimeField(_("data anulowania"), null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="updated_purchase_orders", verbose_name=_("status zmienił"))

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = _("zamówienie zakupu")
        verbose_name_plural = _("zamówienia zakupu")
        constraints = [
            models.CheckConstraint(condition=models.Q(status__in=["new", "preparing", "ready", "shipped", "completed", "cancelled"]), name="purchase_status_valid"),
            models.CheckConstraint(condition=models.Q(subtotal__gte=0, delivery_fee__gte=0, total=models.F("subtotal")+models.F("delivery_fee")), name="purchase_totals_valid"),
            models.CheckConstraint(condition=models.Q(delivery_method__in=["pickup", "courier"]), name="purchase_delivery_valid"),
        ]

    def __str__(self):
        return self.number

    @property
    def number(self):
        return f"SZ-{self.pk:06d}"

    def get_absolute_url(self):
        return reverse("orders:detail", args=[self.reference])

    @property
    def pickup_store(self):
        return dict(zip(PICKUP_KEYS, STORES)).get(self.pickup_location)

    @property
    def can_customer_cancel(self):
        return self.status == self.Status.NEW

    @property
    def progress_steps(self):
        steps = [(self.Status.NEW, _("Przyjęte")), (self.Status.PREPARING, _("Przygotowanie")), (self.Status.READY if self.delivery_method == self.Delivery.PICKUP else self.Status.SHIPPED, _("Odbiór") if self.delivery_method == self.Delivery.PICKUP else _("Wysyłka")), (self.Status.COMPLETED, _("Zakończone"))]
        values = [value for value, _ in steps]
        current = values.index(self.status) if self.status in values else -1
        return [{"label": label, "done": i <= current, "current": i == current} for i, (_, label) in enumerate(steps)]


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT, related_name="purchase_lines", verbose_name=_("produkt"))
    product_name = models.CharField(_("zapisana nazwa sprzętu"), max_length=160)
    size = models.CharField(_("rozmiar"), max_length=80, blank=True)
    size_en = models.CharField(_("rozmiar (angielski)"), max_length=80, blank=True)
    image_path = models.CharField(max_length=240, blank=True)
    unit_price = models.DecimalField(_("cena jednostkowa"), max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(_("Ilość"), validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["pk"]
        verbose_name = _("pozycja zamówienia")
        verbose_name_plural = _("pozycje zamówienia")
        constraints = [
            models.CheckConstraint(condition=models.Q(unit_price__gte=0, quantity__gte=1), name="purchase_line_valid"),
            models.UniqueConstraint(fields=["order", "product"], name="purchase_order_product_unique"),
        ]

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    @property
    def display_size(self):
        from catalog.localization import localized_text
        return localized_text(self, "size")
