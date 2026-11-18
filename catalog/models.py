from django.utils.translation import gettext_lazy as _
from django.db import models
from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.urls import reverse
from django.core.exceptions import ValidationError
from .localization import localized_text
from .taxonomy import SUBCATEGORIES, SkiSubcategory, subcategory_constraint


class Material(models.Model):
    code = models.SlugField(_("identyfikator"), unique=True, max_length=50)
    name = models.CharField(_("nazwa"), max_length=80)
    name_en = models.CharField(_("nazwa (angielski)"), max_length=80, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("materiał")
        verbose_name_plural = _("materiały")

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return localized_text(self, "name")


class SkillLevel(models.Model):
    class Code(models.TextChoices):
        BEGINNER = "beginner", _("Początkujący")
        INTERMEDIATE = "intermediate", _("Średniozaawansowany")
        ADVANCED = "advanced", _("Zaawansowany")

    code = models.CharField(_("poziom zaawansowania"), max_length=16, unique=True, choices=Code.choices)

    class Meta:
        ordering = ["pk"]
        verbose_name = _("poziom zaawansowania")
        verbose_name_plural = _("poziomy zaawansowania")
        constraints = [models.CheckConstraint(condition=models.Q(code__in=["beginner", "intermediate", "advanced"]), name="skill_level_code_valid")]

    def __str__(self):
        return self.get_code_display()

    def get_absolute_url(self):
        return reverse("catalog:skill_level", kwargs={"code": self.code})


class Product(models.Model):
    SkiSubcategory = SkiSubcategory

    class Category(models.TextChoices):
        SKIS = "skis", _("Narty")
        SNOWBOARDS = "snowboards", _("Snowboardy")
        BINDINGS = "bindings", _("Wiązania")
        HELMETS = "helmets", _("Kaski")
        GOGGLES = "goggles", _("Gogle")
        SNOWBOARD_BOOTS = "snowboard_boots", _("Buty snowboardowe")
        BOOTS = "boots", _("Buty narciarskie")
        ACCESSORIES = "accessories", _("Akcesoria")

    name = models.CharField(_("nazwa"), max_length=160)
    slug = models.SlugField(_("adres produktu"), unique=True, max_length=180)
    category = models.CharField(_("kategoria"), max_length=20, choices=Category.choices)
    subcategory = models.CharField(
        _("podkategoria"), max_length=32, blank=True,
        help_text=_("Typ sprzętu właściwy dla wybranej kategorii."),
    )
    description = models.TextField(_("opis"))
    description_en = models.TextField(_("opis (angielski)"), blank=True)
    construction_en = models.TextField(_("konstrukcja (angielski)"), blank=True)
    dimensions_en = models.CharField(_("wymiary (angielski)"), max_length=240, blank=True)
    weight_scope_en = models.CharField(_("masa dotyczy (angielski)"), max_length=120, blank=True)
    size_en = models.CharField(_("rozmiar (angielski)"), max_length=80, blank=True)
    size = models.CharField(_("rozmiar"), max_length=80, blank=True, help_text=_("Z jednostką, np. 172 cm, M (55–59 cm) lub 27,0 MP."))
    materials = models.ManyToManyField(Material, blank=True, related_name="products", verbose_name=_("materiały"))
    skill_levels = models.ManyToManyField(SkillLevel, blank=True, related_name="products", verbose_name=_("poziomy zaawansowania"), help_text=_("Wybierz poziomy, dla których polecasz ten model. Brak wyboru ukrywa go w poradniku tras."))
    construction = models.TextField(_("konstrukcja i zastosowanie materiałów"), blank=True)
    dimensions = models.CharField(_("wymiary"), max_length=240, blank=True, help_text=_("Wpisz jednostki oraz rodzaj pomiaru."))
    weight_g = models.PositiveIntegerField(_("masa (g)"), null=True, blank=True, validators=[MinValueValidator(1)])
    weight_scope = models.CharField(_("masa dotyczy"), max_length=120, blank=True, help_text=_("Np. para nart z wiązaniami, jeden but lub komplet 8 śrub."))
    specifications_are_demo = models.BooleanField(_("parametry demonstracyjne"), default=False)
    price = models.DecimalField(_("cena sprzedaży (zł)"), max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0)])
    discount_percent = models.PositiveSmallIntegerField(_("rabat (%)"), default=0, validators=[MaxValueValidator(99)], help_text=_("0 wyłącza promocję. Rabat naliczany od ceny regularnej produktu."))
    sale_stock = models.PositiveIntegerField(_("liczba sztuk na sprzedaż"), default=0)
    is_active = models.BooleanField(_("widoczny w katalogu"), default=True)
    image_path = models.CharField(
        _("zdjęcie produktu"), max_length=240, blank=True,
        help_text=_("Ścieżka względem static/, np. img/snowboard1.jpg. Puste pole oznacza ilustrację kategorii."),
        validators=[RegexValidator(
            regex=r"\Aimg/(?:[a-zA-Z0-9_-]+/)*[a-zA-Z0-9_-]+\.(?:jpg|jpeg|png|webp)\Z",
            message=_("Podaj ścieżkę w img/ do pliku jpg, jpeg, png lub webp, bez spacji."),
        )],
    )
    featured_order = models.PositiveSmallIntegerField(
        _("kolejność na stronie głównej"), null=True, blank=True,
        help_text=_("Puste: bez wyróżnienia. Niższa liczba: wcześniej. Wymagane zdjęcie; pokazujemy maksymalnie 3 produkty."),
    )
    created_at = models.DateTimeField(_("data dodania"), auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("produkt")
        verbose_name_plural = _("produkty")
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
                message = _("Wybierz podkategorię nart.") if self.category == self.Category.SKIS else _("Wybierz podkategorię produktu.")
                errors.setdefault("subcategory", []).append(message)
            if self.subcategory and self.subcategory not in choices:
                errors.setdefault("subcategory", []).append(_("Ta podkategoria nie pasuje do wybranej kategorii."))
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
    def display_description(self):
        return localized_text(self, "description")

    @property
    def display_construction(self):
        return localized_text(self, "construction")

    @property
    def display_dimensions(self):
        return localized_text(self, "dimensions")

    @property
    def display_weight_scope(self):
        return localized_text(self, "weight_scope")

    @property
    def display_size(self):
        return localized_text(self, "size")

    @property
    def illustration_path(self):
        category = self.category
        if category == self.Category.SNOWBOARD_BOOTS:
            category = "boots"
        elif category in (self.Category.BINDINGS, self.Category.HELMETS, self.Category.GOGGLES):
            category = "accessories"
        return f"img/{category}.svg"
