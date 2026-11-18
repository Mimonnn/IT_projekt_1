from django.urls import path
from . import views

app_name = "catalog"
urlpatterns = [
    path("trasy/<slug:code>/", views.skill_level, name="skill_level"),
    path("regulamin/", views.terms, name="terms"),
    path("kontakt/", views.contact, name="contact"),
    path("sklepy/", views.stores, name="stores"),
    path("", views.home, name="home"),
    path("katalog/", views.product_list, name="list"),
    path("katalog/<slug:slug>/", views.product_detail, name="detail"),
]

