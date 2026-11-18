from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderLine
from .services import can_manage_orders, change_order_status


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ("product_name", "size", "quantity", "unit_price", "line_total")
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description=_("Wartość"))
    def line_total(self, obj):
        return obj.subtotal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "created_at", "delivery_method", "total", "status")
    list_filter = ("status", "delivery_method", "created_at")
    search_fields = ("user__username", "email", "first_name", "last_name")
    readonly_fields = tuple(field.name for field in Order._meta.fields)
    inlines = (OrderLineInline,)
    actions = ("prepare_selected", "ready_selected", "ship_selected", "complete_selected", "cancel_selected")

    @admin.display(description=_("Numer zamówienia"))
    def order_number(self, obj):
        return obj.number

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return obj is None and super().has_change_permission(request, obj)

    def has_manage_permission(self, request):
        return can_manage_orders(request.user)

    def _process(self, request, queryset, target):
        count = 0
        for order in queryset.order_by("pk"):
            try:
                change_order_status(reference=order.reference, user=request.user, target=target, as_staff=True)
            except ValidationError as error:
                self.message_user(request, order.number+": "+" ".join(error.messages), level=messages.ERROR)
            else:
                count += 1
        self.message_user(request, _("Obsłużone zamówienia: %(count)s.") % {"count": count})

    @admin.action(description=_("Rozpocznij przygotowanie"), permissions=["manage"])
    def prepare_selected(self, request, queryset):
        self._process(request, queryset, Order.Status.PREPARING)

    @admin.action(description=_("Oznacz jako gotowe do odbioru"), permissions=["manage"])
    def ready_selected(self, request, queryset):
        self._process(request, queryset, Order.Status.READY)

    @admin.action(description=_("Oznacz jako wysłane"), permissions=["manage"])
    def ship_selected(self, request, queryset):
        self._process(request, queryset, Order.Status.SHIPPED)

    @admin.action(description=_("Zakończ zamówienia"), permissions=["manage"])
    def complete_selected(self, request, queryset):
        self._process(request, queryset, Order.Status.COMPLETED)

    @admin.action(description=_("Anuluj i przywróć produkty na stan"), permissions=["manage"])
    def cancel_selected(self, request, queryset):
        self._process(request, queryset, Order.Status.CANCELLED)
