from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.templatetags.static import static
from .models import Material, Product
from .forms import ProductAdminForm
from .taxonomy import SUBCATEGORIES


class SubcategoryFilter(admin.SimpleListFilter):
    title = _("podkategoria")
    parameter_name = "subcategory"

    def lookups(self, request, model_admin):
        selected = request.GET.get("category__exact")
        for category, choices in SUBCATEGORIES.items():
            if selected and selected != category:
                continue
            category_label = Product.Category(category).label
            for value, label in choices:
                yield f"{category}:{value}", f"{category_label} — {label}"

    def queryset(self, request, queryset):
        if self.value():
            category, _, value = self.value().partition(":")
            return queryset.filter(category=category, subcategory=value)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("name", "category", "display_subcategory", "price", "discount_percent", "sale_stock", "is_active", "featured_order")
    list_editable = ("featured_order",)
    list_filter = ("category", SubcategoryFilter, "materials", "skill_levels", "size", "is_active")
    search_fields = ("name", "description", "construction", "description_en", "construction_en")
    filter_horizontal = ("materials", "skill_levels")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description=_("podkategoria"), ordering="subcategory")
    def display_subcategory(self, obj):
        return obj.get_subcategory_display()

    class Media:
        js = (static("js/admin-subcategories.js") + "?v=1",)


admin.site.site_header = _("Szron — zarządzanie")
admin.site.site_title = _("Szron")
admin.site.index_title = _("Panel administratora")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "name_en", "code")
    search_fields = ("name", "name_en", "code")
    prepopulated_fields = {"code": ("name",)}
