from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("zamowienie/", views.checkout, name="checkout"),
    path("konto/zamowienia/<uuid:reference>/", views.detail, name="detail"),
    path("konto/zamowienia/<uuid:reference>/anuluj/", views.cancel, name="cancel"),
]
