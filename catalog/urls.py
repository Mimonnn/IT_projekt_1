from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("", views.home, name="home"),
    path("katalog/", views.product_list, name="list"),
    path("katalog/<slug:slug>/", views.product_detail, name="detail"),
]

