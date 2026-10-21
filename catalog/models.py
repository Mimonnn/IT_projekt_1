from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.urls import reverse


class Product(models.Model):
    class Category(models.TextChoices):
        SKIS = "skis", "Narty"
        SNOWBOARDS = "snowboards", "Snowboardy"
        BINDINGS = "bindings", "Wiązania"
        HELMETS = "helmets", "Kaski"
        GOGGLES = "goggles", "Gogle"
        SNOWBOARD_BOOTS = "snowboard_boots", "Buty snowboardowe"
        BOOTS = "boots", "Buty narciarskie"
        ACCESSORIES = "accessories", "Akcesoria"

    name = models.CharField("nazwa", max_length=160)
    slug = models.SlugField("adres produktu", unique=True, max_length=180)
    category = models.CharField("kategoria", max_length=20, choices=Category.choices)
    description = models.TextField("opis")
    price = models.DecimalField("cena sprzedaży (zł)", max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    sale_stock = models.PositiveIntegerField("liczba sztuk na sprzedaż", default=0)
    is_active = models.BooleanField("widoczny w katalogu", default=True)
    image_path = models.CharField(
        "zdjęcie produktu", max_length=240, blank=True,
        help_text="Ścieżka względem static/, np. img/snowboard1.jpg. Puste pole oznacza ilustrację kategorii.",
        validators=[RegexValidator(
            regex=r"\Aimg/(?:[a-zA-Z0-9_-]+/)*[a-zA-Z0-9_-]+\.(?:jpg|jpeg|png|webp)\Z",
            message="Podaj ścieżkę w img/ do pliku jpg, jpeg, png lub webp, bez spacji.",
        )],
    )
    featured_order = models.PositiveSmallIntegerField(
        "kolejność na stronie głównej", null=True, blank=True,
        help_text="Puste: bez wyróżnienia. Niższa liczba: wcześniej. Wymagane zdjęcie; pokazujemy maksymalnie 3 produkty.",
    )
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

    @property
    def illustration_path(self):
        category = self.category
        if category == self.Category.SNOWBOARD_BOOTS:
            category = "boots"
        elif category in (self.Category.BINDINGS, self.Category.HELMETS, self.Category.GOGGLES):
            category = "accessories"
        return f"img/{category}.svg"
