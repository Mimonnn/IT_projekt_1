from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


class Product(models.Model):
    class Category(models.TextChoices):
        SKIS = "skis", "Narty"
        BOOTS = "boots", "Buty narciarskie"
        SNOWBOARDS = "snowboards", "Snowboardy"
        ACCESSORIES = "accessories", "Akcesoria"

    name = models.CharField("nazwa", max_length=160)
    slug = models.SlugField("adres produktu", unique=True, max_length=180)
    category = models.CharField("kategoria", max_length=20, choices=Category.choices)
    description = models.TextField("opis")
    price = models.DecimalField("cena sprzedaży (zł)", max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    sale_stock = models.PositiveIntegerField("liczba sztuk na sprzedaż", default=0)
    is_active = models.BooleanField("widoczny w katalogu", default=True)
    created_at = models.DateTimeField("data dodania", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "produkt"
        verbose_name_plural = "produkty"
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gte=0), name="product_price_nonnegative"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:detail", kwargs={"slug": self.slug})
