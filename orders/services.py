from decimal import Decimal
import uuid

from django.contrib.auth import get_user_model
from django.core import signing
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import CartItem
from catalog.models import Product
from .forms import CheckoutForm
from .models import DELIVERY_FEES, PICKUP_KEYS, Order, OrderLine
from catalog.store_info import STORES

QUOTE_SALT = "szron.checkout.v1"


def cart_snapshot(items):
    return [[item.pk, item.product_id, item.quantity, str(item.product.selling_price), item.product.name, item.product.size, item.product.size_en] for item in items]


def make_quote(user, items):
    return signing.dumps({"user": user.pk, "token": str(uuid.uuid4()), "cart": cart_snapshot(items), "fees": {key: str(value) for key, value in DELIVERY_FEES.items()}}, salt=QUOTE_SALT, compress=True)


@transaction.atomic
def place_order(*, user, data, quote):
    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied
    try:
        payload = signing.loads(quote, salt=QUOTE_SALT, max_age=7200)
        token = uuid.UUID(payload["token"])
        if payload["user"] != user.pk:
            raise ValueError
    except (signing.BadSignature, ValueError, KeyError, TypeError):
        raise ValidationError(_("Podsumowanie zamówienia wygasło lub jest nieprawidłowe. Sprawdź koszyk ponownie."))
    # Wspólna kolejność dla zakupów i koszyka: konto, następnie produkty po ID.
    get_user_model().objects.select_for_update(no_key=True).get(pk=user.pk)
    existing = Order.objects.filter(user=user, checkout_token=token).first()
    if existing:
        return existing
    validated = CheckoutForm({**data, "quote": quote})
    if not validated.is_valid():
        raise ValidationError([message for errors in validated.errors.values() for message in errors])
    data = validated.cleaned_data
    items = list(CartItem.objects.filter(user=user).select_related("product").order_by("pk"))
    if not items:
        raise ValidationError(_("Twój koszyk jest pusty."))
    products = {product.pk: product for product in Product.objects.select_for_update().filter(pk__in=[item.product_id for item in items]).order_by("pk")}
    if len(products) != len(items):
        raise ValidationError(_("Koszyk zmienił się. Sprawdź produkty i potwierdź ponownie."))
    for item in items:
        item.product = products[item.product_id]
        if not item.is_available:
            raise ValidationError(_("Produkt %(name)s jest niedostępny w wybranej ilości. Popraw koszyk.") % {"name": item.product.name})
    if payload.get("cart") != cart_snapshot(items) or payload.get("fees") != {key: str(value) for key, value in DELIVERY_FEES.items()}:
        raise ValidationError(_("Koszyk lub cena zmieniły się. Sprawdź aktualne podsumowanie i potwierdź ponownie."))
    method = data["delivery_method"]
    if method not in DELIVERY_FEES:
        raise ValidationError(_("Wybierz prawidłowy sposób dostawy."))
    subtotal = sum((item.subtotal for item in items), Decimal("0.00"))
    fee = DELIVERY_FEES[method]
    pickup_address = dict(zip(PICKUP_KEYS, (store["address"] for store in STORES))).get(data.get("pickup_location"), "") if method == "pickup" else ""
    order = Order.objects.create(pickup_address=pickup_address, user=user, checkout_token=token, subtotal=subtotal, delivery_fee=fee, total=subtotal+fee,
        **{field: data.get(field, "") for field in ("first_name", "last_name", "email", "phone", "delivery_method", "pickup_location", "street_address", "postal_code", "city", "notes")})
    OrderLine.objects.bulk_create([OrderLine(order=order, product=item.product, product_name=item.product.name, size=item.product.size, size_en=item.product.size_en, image_path=item.product.image_path, unit_price=item.product.selling_price, quantity=item.quantity) for item in items])
    for item in items:
        product = item.product
        product.sale_stock -= item.quantity
        product.save(update_fields=["sale_stock"])
    CartItem.objects.filter(user=user, pk__in=[item.pk for item in items]).delete()
    return order


def can_manage_orders(user):
    return user.is_authenticated and user.is_active and user.is_staff and user.has_perms(("orders.change_order", "catalog.change_product"))


@transaction.atomic
def change_order_status(*, reference, user, target, as_staff=False):
    if not user.is_authenticated or not user.is_active:
        raise PermissionDenied
    if as_staff:
        if not can_manage_orders(user):
            raise PermissionDenied
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=user)
        if target != Order.Status.CANCELLED:
            raise PermissionDenied
    order = get_object_or_404(orders.select_for_update(), reference=reference)
    if order.status == target:
        return order
    allowed = {
        Order.Status.NEW: {Order.Status.PREPARING, Order.Status.CANCELLED},
        Order.Status.PREPARING: {Order.Status.READY if order.delivery_method == Order.Delivery.PICKUP else Order.Status.SHIPPED, Order.Status.CANCELLED},
        Order.Status.READY: {Order.Status.COMPLETED, Order.Status.CANCELLED},
        Order.Status.SHIPPED: {Order.Status.COMPLETED},
    }
    if target not in allowed.get(order.status, set()) or (not as_staff and order.status != Order.Status.NEW):
        raise ValidationError(_("Nie można wykonać tej operacji przy obecnym statusie zamówienia."))
    if target == Order.Status.CANCELLED:
        lines = list(order.lines.all())
        products = {product.pk: product for product in Product.objects.select_for_update().filter(pk__in=[line.product_id for line in lines]).order_by("pk")}
        for line in lines:
            product = products[line.product_id]
            product.sale_stock += line.quantity
            product.save(update_fields=["sale_stock"])
        order.cancelled_at = timezone.now()
    if target == Order.Status.COMPLETED:
        order.completed_at = timezone.now()
    order.status = target
    order.updated_by = user
    order.save(update_fields=["status", "updated_by", "updated_at", "cancelled_at", "completed_at"])
    return order
