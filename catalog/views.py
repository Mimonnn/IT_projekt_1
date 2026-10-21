from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Product


def home(request):
    featured_products = Product.objects.filter(
        is_active=True, featured_order__isnull=False,
    ).exclude(image_path="").order_by("featured_order", "pk")[:3]
    return render(request, "catalog/home.html", {
        "featured_products": featured_products,
        "hero_categories": [(value, label) for value, label in Product.Category.choices
                            if value != Product.Category.ACCESSORIES],
        "hero_slides": [
            ("img/hero/panorama1.jpg", "Ośnieżony stok i wyciągi wśród zimowego lasu"),
            ("img/hero/panorama2.jpg", "Narciarki podziwiające zimową panoramę gór"),
            ("img/hero/panorama3.jpg", "Narciarz w skoku na tle alpejskich szczytów"),
            ("img/hero/panorama4.jpg", "Ośnieżona grań i trasa narciarska pośród chmur"),
        ],
    })


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
