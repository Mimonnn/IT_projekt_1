from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "sale_stock", "is_active", "featured_order")
    list_editable = ("featured_order",)
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


admin.site.site_header = "Szron — zarządzanie"
admin.site.site_title = "Szron"
admin.site.index_title = "Panel administratora"
