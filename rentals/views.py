from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST, require_http_methods

from .forms import RentalDatesForm
from .services import cancel_reservation, overlapping_reservations, reserve_item

from catalog.models import Product
from .models import RentalItem, Reservation


def item_list(request):
    # Opcje pochodzą wyłącznie z publicznych egzemplarzy wypożyczalni.
    visible_items = list(RentalItem.objects.filter(
        is_active=True, product__is_active=True,
    ).select_related("product"))
    issued_ids = set(Reservation.objects.filter(status=Reservation.Status.ISSUED).values_list("item_id", flat=True))
    category = request.GET.get("category", "")[:20]
    model = request.GET.get("model", "")[:180]
    size = request.GET.get("size", "")[:80]
    category_items = [item for item in visible_items if not category or item.product.category == category]
    models = sorted({item.product.slug: item.product.name for item in category_items}.items(), key=lambda row: row[1])
    model_items = [item for item in category_items if not model or item.product.slug == model]
    sizes = sorted({item.size: item.display_size for item in model_items}.items(), key=lambda row: row[1])
    items = [item for item in model_items if not size or item.size == size]
    detail_query = urlencode({key: request.GET[key] for key in ("category", "model", "size", "start_date", "end_date") if request.GET.get(key)})
    dates_requested = bool(request.GET.get("start_date") or request.GET.get("end_date"))
    date_form = RentalDatesForm(request.GET if dates_requested else None)
    valid_dates = date_form.is_valid() if dates_requested else False
    days, date_query = None, ""
    if valid_dates:
        start, end = date_form.cleaned_data["start_date"], date_form.cleaned_data["end_date"]
        blocked = set(overlapping_reservations(start, end).values_list("item_id", flat=True))
        items = [item for item in items if item.status == RentalItem.Status.AVAILABLE and item.pk not in blocked]
        days = (end - start).days + 1
        date_query = urlencode({"start_date": start.isoformat(), "end_date": end.isoformat()})
    for item in items:
        item.can_reserve = item.status == RentalItem.Status.AVAILABLE and item.pk not in issued_ids and (not dates_requested or valid_dates)
        item.period_price = item.daily_rate * days if days else None
    # Dane dla JS nie zawierają notatek ani numerów ewidencyjnych.
    options = list({(item.product.slug, item.size): {
        "category": item.product.category, "model": item.product.slug,
        "name": item.product.name, "size": item.size, "size_label": item.display_size,
    } for item in visible_items}.values())
    return render(request, "rentals/item_list.html", {
        "items": items, "categories": Product.Category.choices,
        "selected_category": category, "selected_model": model, "selected_size": size,
        "models": models, "sizes": sizes,
        "model_values": [value for value, _ in models],
        "size_values": [value for value, _ in sizes],
        "rental_options": options, "detail_query": detail_query, "date_form": date_form, "days": days, "date_query": date_query,
    })


@login_required
@require_http_methods(["GET", "POST"])
def reserve(request, pk):
    item = get_object_or_404(RentalItem.objects.select_related("product"), pk=pk, is_active=True, product__is_active=True)
    date_form = RentalDatesForm(request.POST if request.method == "POST" else (request.GET or None))
    checked = date_form.is_bound and date_form.is_valid()
    available, total, days = False, None, None
    if checked:
        start, end = date_form.cleaned_data["start_date"], date_form.cleaned_data["end_date"]
        days = (end - start).days + 1
        total = item.daily_rate * days
        available = item.status == RentalItem.Status.AVAILABLE and not overlapping_reservations(start, end).filter(item=item).exists()
        if request.method == "POST":
            try:
                quoted_rate = Decimal(request.POST.get("quoted_rate", ""))
                if not quoted_rate.is_finite():
                    raise InvalidOperation
            except (InvalidOperation, ValueError):
                date_form.add_error(None, _("Sprawdź cenę przed potwierdzeniem rezerwacji."))
            else:
                try:
                    reserve_item(user=request.user, item_id=item.pk, start_date=start, end_date=end, quoted_rate=quoted_rate)
                except ValidationError as error:
                    date_form.add_error(None, error)
                    item.refresh_from_db()
                    total = item.daily_rate * days
                    available = False
                else:
                    messages.success(request, _("Rezerwacja została zapisana. Znajdziesz ją w zakładce Moje wypożyczenia."))
                    return redirect("rentals:mine")
    return render(request, "rentals/reserve.html", {"item": item, "date_form": date_form,
        "available": available, "checked": checked, "days": days, "total": total})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "rentals/my_reservations.html", {"reservations": reservations, "active_tab": "rentals"})


@login_required
@require_POST
def cancel(request, pk):
    try:
        cancel_reservation(reservation_id=pk, user=request.user)
    except ValidationError as error:
        messages.error(request, " ".join(error.messages))
    else:
        messages.success(request, _("Rezerwacja została anulowana."))
    return redirect("rentals:mine")


def item_detail(request, pk):
    item = get_object_or_404(
        RentalItem.objects.select_related("product").prefetch_related("product__materials"),
        pk=pk, is_active=True, product__is_active=True,
    )
    dates_requested = bool(request.GET.get("start_date") or request.GET.get("end_date"))
    date_form = RentalDatesForm(request.GET if dates_requested else None)
    valid_dates = date_form.is_valid() if dates_requested else False
    available = item.status == RentalItem.Status.AVAILABLE and not item.reservations.filter(status=Reservation.Status.ISSUED).exists()
    days, total, date_query = None, None, ""
    if valid_dates:
        start, end = date_form.cleaned_data["start_date"], date_form.cleaned_data["end_date"]
        days = (end - start).days + 1
        total = item.daily_rate * days
        available = available and not overlapping_reservations(start, end).filter(item=item).exists()
        date_query = urlencode({"start_date": start.isoformat(), "end_date": end.isoformat()})
    elif dates_requested:
        available = False
    back_filters = {key: request.GET[key] for key in ("category", "model", "size") if request.GET.get(key)}
    back_query = urlencode(back_filters | {key: request.GET[key] for key in ("start_date", "end_date") if request.GET.get(key)})
    return render(request, "rentals/item_detail.html", {
        "item": item, "product": item.product, "date_form": date_form,
        "available": available, "valid_dates": valid_dates, "days": days, "total": total,
        "date_query": date_query, "back_query": back_query, "back_filters": back_filters,
    })
