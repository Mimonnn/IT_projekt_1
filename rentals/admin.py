from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import RentalItem, Reservation
from .services import cancel_reservation, can_operate_rentals, issue_reservation, return_reservation


@admin.register(RentalItem)
class RentalItemAdmin(admin.ModelAdmin):
    list_display = ("inventory_code", "product", "size", "daily_rate", "status", "is_active")
    list_filter = ("status", "is_active", "product__category")
    search_fields = ("inventory_code", "product__name", "size", "technical_notes")
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at",)
    fields = ("product", "inventory_code", "size", "size_en", "daily_rate", "status", "is_active", "technical_notes", "created_at")

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.reservations.filter(status=Reservation.Status.ISSUED).exists():
            return (*self.readonly_fields, "status", "product", "inventory_code", "size", "size_en")
        return self.readonly_fields


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item", "start_date", "end_date", "daily_rate", "status", "issued_at", "returned_at")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("user__username", "item__inventory_code", "product_name")
    readonly_fields = ("user", "item", "product_name", "size", "size_en", "start_date", "end_date", "daily_rate", "status", "created_at", "cancelled_at", "issued_at", "issued_by", "returned_at", "returned_by", "returned_to_service")
    fields = readonly_fields
    actions = ("issue_selected", "return_selected", "return_to_service_selected", "cancel_selected")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        # Historia jest tylko do odczytu; uprawnienie na liście pozwala użyć akcji.
        return obj is None and super().has_change_permission(request, obj)

    @admin.action(description=_("Anuluj zaznaczone rezerwacje"), permissions=["change"])
    def cancel_selected(self, request, queryset):
        for reservation in queryset.order_by("item_id", "pk"):
            try:
                cancel_reservation(reservation_id=reservation.pk, user=request.user, as_staff=True)
            except ValidationError as error:
                self.message_user(request, " ".join(error.messages), level=messages.ERROR)
        self.message_user(request, _("Zakończono anulowanie zaznaczonych rezerwacji."))


    def has_operate_permission(self, request):
        return can_operate_rentals(request.user)

    def _process_handover(self, request, queryset, operation, **kwargs):
        succeeded = 0
        for reservation in queryset.order_by("item_id", "pk"):
            try:
                operation(reservation_id=reservation.pk, user=request.user, **kwargs)
            except ValidationError as error:
                self.message_user(request, f"#{reservation.pk}: " + " ".join(error.messages), level=messages.ERROR)
            else:
                succeeded += 1
        self.message_user(request, _("Obsłużone rezerwacje: %(count)s.") % {"count": succeeded})

    @admin.action(description=_("Wydaj sprzęt z zaznaczonych rezerwacji"), permissions=["operate"])
    def issue_selected(self, request, queryset):
        self._process_handover(request, queryset, issue_reservation)

    @admin.action(description=_("Przyjmij zwrot — sprzęt na stan"), permissions=["operate"])
    def return_selected(self, request, queryset):
        self._process_handover(request, queryset, return_reservation)

    @admin.action(description=_("Przyjmij zwrot — sprzęt do serwisu"), permissions=["operate"])
    def return_to_service_selected(self, request, queryset):
        self._process_handover(request, queryset, return_reservation, to_service=True)
