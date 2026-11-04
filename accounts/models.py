from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Własny model od początku ułatwi późniejszą rozbudowę kont klientów."""
    phone = models.CharField(_("numer telefonu"), max_length=25, blank=True, validators=[RegexValidator(
        regex=r"\A\+?[0-9][0-9 ()-]{5,23}[0-9]\Z", message=_("Podaj numer telefonu złożony z 7–25 znaków: cyfr, spacji, nawiasów, myślników i opcjonalnego + na początku."),
    )])

    class Meta(AbstractUser.Meta):
        verbose_name = _("użytkownik")
        verbose_name_plural = _("użytkownicy")


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="favorite_unique_user_product")]


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["pk"]
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="cart_unique_user_product"),
            models.CheckConstraint(condition=models.Q(quantity__gte=1), name="cart_positive_quantity"),
        ]

    @property
    def subtotal(self):
        return self.product.selling_price * self.quantity

    @property
    def is_available(self):
        return self.product.is_active and self.quantity <= self.product.sale_stock
