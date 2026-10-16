from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product


def home(request):
    products = Product.objects.filter(is_active=True)[:3]
    return render(request, "catalog/home.html", {"products": products})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()[:100]
    if category:
        products = products.filter(category=category)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, "catalog/product_list.html", {
        "products": products, "categories": Product.Category.choices,
        "selected_category": category, "query": query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "catalog/product_detail.html", {"product": product})
