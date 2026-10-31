from decimal import Decimal
from urllib.parse import urlsplit

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.debug import sensitive_post_parameters

from catalog.models import Product
from .forms import CartQuantityForm, LoginForm, ProfileForm, RegistrationForm
from .models import CartItem, Favorite


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        # Django weryfikuje host i schemat parametru next przed jego użyciem.
        target = self.get_redirect_url()
        if target and not (not self.request.user.is_staff and urlsplit(target).path.startswith("/admin")):
            return target
        return reverse("admin:index" if self.request.user.is_staff else "accounts:orders")


@sensitive_post_parameters("password1", "password2")
def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:orders")
    form = RegistrationForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Konto zostało utworzone. Witaj w Szron!")
        return redirect("accounts:orders")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def orders(request):
    return render(request, "accounts/profile.html", {"active_tab": "orders"})


@login_required
def history(request):
    return render(request, "accounts/profile.html", {"active_tab": "history"})


@login_required
def returns(request):
    return render(request, "accounts/returns.html", {"active_tab": "returns"})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST if request.method == "POST" else None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        # Zapisujemy tylko dozwolone pola, nigdy flagi konta z żądania.
        user = form.save(commit=False)
        user.save(update_fields=list(form.Meta.fields))
        messages.success(request, "Dane profilu zostały zapisane.")
        return redirect("accounts:edit_profile")
    return render(request, "accounts/edit_profile.html", {"form": form, "active_tab": "profile"})


@login_required
def favorites(request):
    products = Product.objects.filter(is_active=True, favorite__user=request.user).order_by("-favorite__created_at", "-favorite__pk")
    return render(request, "accounts/favorites.html", {"products": products, "active_tab": "favorites"})


@login_required
@require_POST
def favorite_add(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    Favorite.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"Zapisano w ulubionych: {product.name}.")
    return redirect("accounts:favorites")


@login_required
@require_POST
def favorite_remove(request, slug):
    get_object_or_404(Favorite, user=request.user, product__slug=slug).delete()
    messages.success(request, "Usunięto produkt z ulubionych.")
    return redirect("accounts:favorites")


@login_required
def cart(request):
    items = list(request.user.cart_items.select_related("product"))
    return render(request, "accounts/cart.html", {
        "active_tab": "cart", "items": items,
        "total": sum((item.subtotal for item in items), Decimal("0.00")),
    })


@login_required
@require_POST
@transaction.atomic
def cart_add(request, slug):
    # Koszyk nie rezerwuje sztuk i nie zmienia magazynu.
    # Blokada serializuje dodawanie tej samej pozycji do koszyka.
    product = get_object_or_404(Product.objects.select_for_update(), slug=slug, is_active=True)
    form = CartQuantityForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Podaj poprawną, dodatnią liczbę sztuk.")
        return redirect(product)
    item = CartItem.objects.filter(user=request.user, product=product).first()
    quantity = (item.quantity if item else 0) + form.cleaned_data["quantity"]
    if quantity > product.sale_stock:
        messages.error(request, "Nie można dodać tylu sztuk. Sprawdź dostępność i ilość w koszyku.")
        return redirect(product)
    if item:
        item.quantity = quantity
        item.save(update_fields=["quantity"])
    else:
        CartItem.objects.create(user=request.user, product=product, quantity=quantity)
    messages.success(request, f"Dodano do koszyka: {product.name}.")
    return redirect("accounts:cart")


@login_required
@require_POST
@transaction.atomic
def cart_update(request, pk):
    item = get_object_or_404(CartItem.objects.filter(user=request.user), pk=pk)
    product = get_object_or_404(Product.objects.select_for_update(), pk=item.product_id)
    # Podczas czekania na blokadę inna karta mogła usunąć tę pozycję.
    item = get_object_or_404(CartItem.objects.filter(user=request.user), pk=pk)
    form = CartQuantityForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Podaj poprawną, dodatnią liczbę sztuk.")
    elif not product.is_active or form.cleaned_data["quantity"] > product.sale_stock:
        messages.error(request, "Wybrana ilość produktu jest obecnie niedostępna.")
    else:
        item.quantity = form.cleaned_data["quantity"]
        item.save(update_fields=["quantity"])
        messages.success(request, "Zmieniono ilość w koszyku.")
    return redirect("accounts:cart")


@login_required
@require_POST
@transaction.atomic
def cart_remove(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    # Każda modyfikacja koszyka blokuje najpierw ten sam produkt.
    get_object_or_404(Product.objects.select_for_update(), pk=item.product_id)
    get_object_or_404(CartItem, pk=pk, user=request.user).delete()
    messages.success(request, "Usunięto produkt z koszyka.")
    return redirect("accounts:cart")
