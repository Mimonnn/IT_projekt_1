from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from accounts.models import CartItem
from .forms import CheckoutForm
from .models import DELIVERY_FEES, Order
from .services import change_order_status, make_quote, place_order


@login_required
@never_cache
@require_http_methods(["GET", "POST"])
@sensitive_post_parameters("first_name", "last_name", "email", "phone", "street_address", "postal_code", "city", "notes")
def checkout(request):
    items = list(CartItem.objects.filter(user=request.user).select_related("product").order_by("pk"))
    if not items and request.method == "GET":
        messages.info(request, _("Dodaj produkty do koszyka, aby złożyć zamówienie."))
        return redirect("accounts:cart")
    initial = {field: getattr(request.user, field) for field in ("first_name", "last_name", "email", "phone")}
    initial["quote"] = make_quote(request.user, items)
    form = CheckoutForm(request.POST if request.method == "POST" else None, initial=initial)
    if request.method == "POST" and form.is_valid():
        try:
            order = place_order(user=request.user, data=form.cleaned_data, quote=form.cleaned_data["quote"])
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, _("Zamówienie %(number)s zostało zapisane. Dziękujemy!") % {"number": order.number})
            return redirect(order.get_absolute_url()+"?placed=1")
    # Po zmianie ceny lub koszyka pokazujemy aktualne dane i wymagamy ponownego potwierdzenia.
    items = list(CartItem.objects.filter(user=request.user).select_related("product").order_by("pk"))
    if form.is_bound:
        updated = form.data.copy()
        updated["quote"] = make_quote(request.user, items)
        form.data = updated
    subtotal = sum((item.subtotal for item in items), Decimal("0.00"))
    method = form["delivery_method"].value() or Order.Delivery.PICKUP
    fee = DELIVERY_FEES.get(method, Decimal("0.00"))
    return render(request, "orders/checkout.html", {"form": form, "items": items, "subtotal": subtotal,
        "delivery_fee": fee, "total": subtotal+fee, "can_checkout": bool(items) and all(item.is_available for item in items),
        "pricing": {"subtotal": str(subtotal), "fees": {key: str(value) for key, value in DELIVERY_FEES.items()}},
        "active_tab": "cart", "courier_fee": DELIVERY_FEES["courier"]})


@login_required
@never_cache
@require_GET
def detail(request, reference):
    order = get_object_or_404(Order.objects.prefetch_related("lines"), reference=reference, user=request.user)
    return render(request, "orders/detail.html", {"order": order, "placed": request.GET.get("placed") == "1", "active_tab": "history" if order.status in (Order.Status.COMPLETED, Order.Status.CANCELLED) else "orders",
        "back_url": reverse("accounts:history" if order.status in (Order.Status.COMPLETED, Order.Status.CANCELLED) else "accounts:orders")})


@login_required
@require_POST
def cancel(request, reference):
    try:
        order = change_order_status(reference=reference, user=request.user, target=Order.Status.CANCELLED)
    except ValidationError as error:
        messages.error(request, " ".join(error.messages))
        return redirect("orders:detail", reference=reference)
    messages.success(request, _("Zamówienie zostało anulowane, a produkty wróciły na stan."))
    return redirect(order)
