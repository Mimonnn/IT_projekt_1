from django.utils.translation import gettext as _
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Material, Product
from .taxonomy import ALL_LABELS, SUBCATEGORIES
from .skill_levels import LEVEL_GUIDES


def home(request):
    featured_products = Product.objects.filter(
        is_active=True, featured_order__isnull=False,
    ).exclude(image_path="").order_by("featured_order", "pk")[:3]
    return render(request, "catalog/home.html", {
        "skill_guides": LEVEL_GUIDES.items(),
        "featured_products": featured_products,
        "promotion_products": Product.objects.filter(is_active=True, sale_stock__gt=0, discount_percent__gt=0).order_by("discount_percent", "pk")[:3],
        "category_menus": [
            {"value": value, "label": _("Snowboard") if value == "snowboards" else label,
             "all_label": ALL_LABELS[value], "subcategories": SUBCATEGORIES[value]}
            for value, label in Product.Category.choices if value in SUBCATEGORIES
        ],
        "hero_categories": [(value, label) for value, label in Product.Category.choices
                            if value != Product.Category.ACCESSORIES],
        "hero_slides": [
            ("img/hero/panorama1.jpg", _("Ośnieżony stok i wyciągi wśród zimowego lasu")),
            ("img/hero/panorama2.jpg", _("Narciarki podziwiające zimową panoramę gór")),
            ("img/hero/panorama3.jpg", _("Narciarz w skoku na tle alpejskich szczytów")),
            ("img/hero/panorama4.jpg", _("Ośnieżona grań i trasa narciarska pośród chmur")),
        ],
    })


def skill_level(request, code):
    from django.http import Http404
    from rentals.models import RentalItem

    if code not in LEVEL_GUIDES:
        raise Http404
    products = Product.objects.filter(is_active=True, skill_levels__code=code)
    # Wydany sprzęt blokuje rezerwację także po planowanej dacie zwrotu.
    items = RentalItem.objects.filter(
        is_active=True, product__in=products, status=RentalItem.Status.AVAILABLE,
    ).exclude(reservations__status="issued").select_related("product")
    category = request.GET.get("category", "")
    if category not in Product.Category.values:
        category = ""
    if category:
        products = products.filter(category=category)
        items = items.filter(product__category=category)
    return render(request, "catalog/skill_level.html", {
        "guide": LEVEL_GUIDES[code], "level_code": code,
        "skill_guides": LEVEL_GUIDES.items(),
        "products": products.filter(sale_stock__gt=0), "items": items,
        "categories": Product.Category.choices, "selected_category": category,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True).prefetch_related("materials")
    category = request.GET.get("category", "")
    subcategory = request.GET.get("subcategory", "") if category in SUBCATEGORIES else ""
    # Zachowujemy działanie dotychczasowych odnośników do nart.
    if category == Product.Category.SKIS and "subcategory" not in request.GET:
        subcategory = request.GET.get("ski_subcategory", "")
    query = request.GET.get("q", "").strip()[:100]
    size = request.GET.get("size", "").strip()[:80]
    material = request.GET.get("material", "").strip()[:50]
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(construction__icontains=query) | Q(description_en__icontains=query) | Q(construction_en__icontains=query))
    specification_options = [
        {"category": item.category, "subcategory": item.subcategory, "size": item.size, "size_label": item.display_size,
         "materials": [(material.code, material.display_name) for material in item.materials.all()]}
        for item in products
    ]
    if category:
        products = products.filter(category=category)
    if subcategory:
        products = products.filter(subcategory=subcategory)
    # Rozmiary i materiały wynikają z kategorii, typu i wyszukiwania;
    # nie zawężamy opcji wybranym rozmiarem lub materiałem.
    size_options = list(products.exclude(size="").order_by("size").values_list("size", flat=True).distinct())
    size_labels = {item.size: item.display_size for item in products}
    material_options = list(Material.objects.filter(products__in=products).distinct())
    if size:
        products = products.filter(size=size)
    if material:
        products = products.filter(materials__code=material)
    return render(request, "catalog/product_list.html", {
        "products": products, "categories": Product.Category.choices,
        "selected_category": category, "query": query,
        "subcategory_options": SUBCATEGORIES,
        "subcategories": SUBCATEGORIES.get(category, []),
        "selected_subcategory": subcategory,
        "sizes": size_options, "size_choices": [(size, size_labels[size]) for size in size_options], "materials": material_options,
        "selected_size": size, "selected_material": material,
        "material_codes": [item.code for item in material_options],
        "specification_options": specification_options,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("materials"), slug=slug, is_active=True)
    is_favorite = request.user.is_authenticated and request.user.favorites.filter(product=product).exists()
    return render(request, "catalog/product_detail.html", {"product": product, "is_favorite": is_favorite})


def terms(request):
    return render(request, "catalog/terms.html")


def contact(request):
    from .store_info import SUPPORT
    return render(request, "catalog/contact.html", {"support": SUPPORT})


def stores(request):
    from .store_info import STORES
    return render(request, "catalog/stores.html", {"stores": STORES})
