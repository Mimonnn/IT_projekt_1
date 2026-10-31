from django.db import models
from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.urls import reverse
from django.core.exceptions import ValidationError
from .taxonomy import SUBCATEGORIES, SkiSubcategory, subcategory_constraint


class Material(models.Model):
    code = models.SlugField("identyfikator", unique=True, max_length=50)
    name = models.CharField("nazwa", max_length=80)

    class Meta:
        ordering = ["name"]
        verbose_name = "materiał"
        verbose_name_plural = "materiały"

    def __str__(self):
        return self.name


class Product(models.Model):
    SkiSubcategory = SkiSubcategory

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
    subcategory = models.CharField(
        "podkategoria", max_length=32, blank=True,
        help_text="Typ sprzętu właściwy dla wybranej kategorii.",
    )
    description = models.TextField("opis")
    size = models.CharField("rozmiar", max_length=80, blank=True, help_text="Z jednostką, np. 172 cm, M (55–59 cm) lub 27,0 MP.")
    materials = models.ManyToManyField(Material, blank=True, related_name="products", verbose_name="materiały")
    construction = models.TextField("konstrukcja i zastosowanie materiałów", blank=True)
    dimensions = models.CharField("wymiary", max_length=240, blank=True, help_text="Wpisz jednostki oraz rodzaj pomiaru.")
    weight_g = models.PositiveIntegerField("masa (g)", null=True, blank=True, validators=[MinValueValidator(1)])
    weight_scope = models.CharField("masa dotyczy", max_length=120, blank=True, help_text="Np. para nart z wiązaniami, jeden but lub komplet 8 śrub.")
    specifications_are_demo = models.BooleanField("parametry demonstracyjne", default=False)
    price = models.DecimalField("cena sprzedaży (zł)", max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    discount_percent = models.PositiveSmallIntegerField("rabat (%)", default=0, validators=[MaxValueValidator(99)], help_text="0 wyłącza promocję. Rabat naliczany od ceny regularnej produktu.")
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
            models.CheckConstraint(condition=models.Q(discount_percent__gte=0, discount_percent__lte=99), name="product_discount_valid"),
            models.CheckConstraint(condition=models.Q(weight_g__isnull=True) | models.Q(weight_g__gt=0), name="product_weight_positive"),
            models.CheckConstraint(
                condition=subcategory_constraint(), name="product_subcategory_valid",
            ),
        ]

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        errors = {}
        try:
            super().clean_fields(exclude=exclude)
        except ValidationError as error:
            errors.update(error.message_dict)
        # Edycja samego wyróżnienia na liście nie zawiera pola podkategorii.
        # Respektujemy wyłączenia formularza; pełna edycja nadal wymaga typu.
        if "subcategory" not in (exclude or ()):
            choices = dict(SUBCATEGORIES.get(self.category, []))
            if choices and not self.subcategory:
                message = "Wybierz podkategorię nart." if self.category == self.Category.SKIS else "Wybierz podkategorię produktu."
                errors.setdefault("subcategory", []).append(message)
            if self.subcategory and self.subcategory not in choices:
                errors.setdefault("subcategory", []).append("Ta podkategoria nie pasuje do wybranej kategorii.")
        if errors:
            raise ValidationError(errors)

    def get_subcategory_display(self):
        return dict(SUBCATEGORIES.get(self.category, [])).get(self.subcategory, self.subcategory)

    def get_absolute_url(self):
        return reverse("catalog:detail", kwargs={"slug": self.slug})

    @property
    def selling_price(self):
        return (Decimal(self.price) * (Decimal(100) - self.discount_percent) / Decimal(100)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def savings(self):
        return Decimal(self.price) - self.selling_price

    @property
    def illustration_path(self):
        category = self.category
        if category == self.Category.SNOWBOARD_BOOTS:
            category = "boots"
        elif category in (self.Category.BINDINGS, self.Category.HELMETS, self.Category.GOGGLES):
            category = "accessories"
        return f"img/{category}.svg"
