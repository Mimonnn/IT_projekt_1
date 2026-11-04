from decimal import Decimal

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _

from .forms import RentalDatesForm
from .models import RentalItem, Reservation


def overlapping_reservations(start_date, end_date):
    # Obie granice są wliczone: zwrot 12. dnia pozwala na kolejny odbiór 13. dnia.
    return Reservation.objects.filter(
        Q(status=Reservation.Status.CONFIRMED, start_date__lte=end_date, end_date__gte=start_date)
        | Q(status=Reservation.Status.ISSUED)
    )


@transaction.atomic
def reserve_item(*, user, item_id, start_date, end_date, quoted_rate):
    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied
    dates = RentalDatesForm({"start_date": start_date, "end_date": end_date})
    if not dates.is_valid():
        raise ValidationError([message for messages in dates.errors.values() for message in messages])
    start_date, end_date = dates.cleaned_data["start_date"], dates.cleaned_data["end_date"]
    # Każdy zapis i anulowanie blokują najpierw ten sam wiersz egzemplarza.
    # Drugie równoczesne żądanie sprawdza kolizje dopiero po zakończeniu pierwszego.
    item = get_object_or_404(RentalItem.objects.select_for_update(of=("self",)).select_related("product"), pk=item_id)
    if not item.is_active or not item.product.is_active or item.status != RentalItem.Status.AVAILABLE:
        raise ValidationError(_("Ten egzemplarz nie jest obecnie dostępny do rezerwacji."))
    existing = item.reservations.filter(user=user, status=Reservation.Status.CONFIRMED, start_date=start_date, end_date=end_date).first()
    if existing:
        return existing
    if overlapping_reservations(start_date, end_date).filter(item=item).exists():
        raise ValidationError(_("Ten egzemplarz został już zarezerwowany w wybranym terminie. Wybierz inny termin lub egzemplarz."))
    if quoted_rate != item.daily_rate:
        raise ValidationError(_("Stawka zmieniła się. Sprawdź ponownie cenę przed potwierdzeniem rezerwacji."))
    return Reservation.objects.create(user=user, item=item, start_date=start_date, end_date=end_date,
        daily_rate=Decimal(item.daily_rate), product_name=item.product.name, size=item.size, size_en=item.size_en)


@transaction.atomic
def cancel_reservation(*, reservation_id, user, as_staff=False):
    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied
    if as_staff:
        if not user.is_active or not user.is_staff or not user.has_perm("rentals.change_reservation"):
            raise PermissionDenied
        owned = Reservation.objects.all()
    else:
        owned = Reservation.objects.filter(user=user)
    initial = get_object_or_404(owned, pk=reservation_id)
    RentalItem.objects.select_for_update().get(pk=initial.item_id)
    reservation = get_object_or_404(owned.select_for_update(), pk=reservation_id)
    if reservation.status == Reservation.Status.CANCELLED:
        return reservation
    if reservation.status != Reservation.Status.CONFIRMED:
        raise ValidationError(_("Wydanego lub zwróconego wypożyczenia nie można anulować."))
    if reservation.start_date < timezone.localdate():
        raise ValidationError(_("Nie można anulować rezerwacji, której termin już się rozpoczął."))
    reservation.status = Reservation.Status.CANCELLED
    reservation.cancelled_at = timezone.now()
    reservation.save(update_fields=["status", "cancelled_at"])
    return reservation


def can_operate_rentals(user):
    return user.is_authenticated and user.is_active and user.is_staff and user.has_perms(("rentals.change_reservation", "rentals.change_rentalitem"))


def _lock_handover(reservation_id):
    initial = get_object_or_404(Reservation, pk=reservation_id)
    item = RentalItem.objects.select_for_update().get(pk=initial.item_id)
    reservation = Reservation.objects.select_for_update().get(pk=initial.pk)
    return item, reservation


@transaction.atomic
def issue_reservation(*, reservation_id, user):
    if not can_operate_rentals(user):
        raise PermissionDenied
    item, reservation = _lock_handover(reservation_id)
    if reservation.status == Reservation.Status.ISSUED:
        return reservation
    if reservation.status != Reservation.Status.CONFIRMED:
        raise ValidationError(_("Wydać można tylko sprzęt z potwierdzonej rezerwacji."))
    today = timezone.localdate()
    if not reservation.start_date <= today <= reservation.end_date:
        raise ValidationError(_("Sprzęt można wydać tylko w zarezerwowanym okresie."))
    if not item.is_active or not item.product.is_active or item.status != RentalItem.Status.AVAILABLE:
        raise ValidationError(_("Sprzęt nie jest gotowy do wydania. Sprawdź jego stan i widoczność."))
    if overlapping_reservations(reservation.start_date, reservation.end_date).filter(item=item).exclude(pk=reservation.pk).exists():
        raise ValidationError(_("Inne wypożyczenie lub rezerwacja blokuje wydanie tego egzemplarza."))
    reservation.status = Reservation.Status.ISSUED
    reservation.issued_at = timezone.now()
    reservation.issued_by = user
    reservation.save(update_fields=["status", "issued_at", "issued_by"])
    item.status = RentalItem.Status.RENTED
    item.save(update_fields=["status"])
    return reservation


@transaction.atomic
def return_reservation(*, reservation_id, user, to_service=False):
    if not can_operate_rentals(user):
        raise PermissionDenied
    item, reservation = _lock_handover(reservation_id)
    if reservation.status == Reservation.Status.RETURNED:
        if reservation.returned_to_service != to_service:
            raise ValidationError(_("Zwrot został już zapisany z innym stanem sprzętu. Dalszy serwis obsłuż w ewidencji egzemplarzy."))
        return reservation
    if reservation.status != Reservation.Status.ISSUED:
        raise ValidationError(_("Przyjąć zwrot można tylko po wydaniu sprzętu."))
    reservation.status = Reservation.Status.RETURNED
    reservation.returned_at = timezone.now()
    reservation.returned_by = user
    reservation.returned_to_service = to_service
    reservation.save(update_fields=["status", "returned_at", "returned_by", "returned_to_service"])
    item.status = RentalItem.Status.SERVICE if to_service else RentalItem.Status.AVAILABLE
    item.save(update_fields=["status"])
    return reservation
