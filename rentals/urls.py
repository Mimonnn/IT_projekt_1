from django.urls import path

from . import views

app_name = "rentals"
urlpatterns = [
    path("wypozyczalnia/", views.item_list, name="list"),
    path("wypozyczalnia/<int:pk>/", views.item_detail, name="detail"),
    path("wypozyczalnia/<int:pk>/rezerwuj/", views.reserve, name="reserve"),
    path("konto/wypozyczenia/", views.my_reservations, name="mine"),
    path("konto/wypozyczenia/<int:pk>/anuluj/", views.cancel, name="cancel"),
]
