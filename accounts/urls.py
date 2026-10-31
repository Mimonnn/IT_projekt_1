from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "accounts"
urlpatterns = [
    path("zaloguj/", views.AccountLoginView.as_view(), name="login"),
    path("zarejestruj/", views.register, name="register"),
    path("wyloguj/", LogoutView.as_view(), name="logout"),
    path("konto/", RedirectView.as_view(pattern_name="accounts:orders", permanent=False), name="profile"),
    path("konto/zamowienia/", views.orders, name="orders"),
    path("konto/historia/", views.history, name="history"),
    path("konto/zwroty/", views.returns, name="returns"),
    path("konto/dane/", views.edit_profile, name="edit_profile"),
    path("konto/ulubione/", views.favorites, name="favorites"),
    path("konto/ulubione/dodaj/<slug:slug>/", views.favorite_add, name="favorite_add"),
    path("konto/ulubione/usun/<slug:slug>/", views.favorite_remove, name="favorite_remove"),
    path("konto/koszyk/", views.cart, name="cart"),
    path("konto/koszyk/dodaj/<slug:slug>/", views.cart_add, name="cart_add"),
    path("konto/koszyk/<int:pk>/ilosc/", views.cart_update, name="cart_update"),
    path("konto/koszyk/<int:pk>/usun/", views.cart_remove, name="cart_remove"),
]
