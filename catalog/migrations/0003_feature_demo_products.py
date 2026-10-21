from django.db import migrations


def feature_demo_products(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    for slug, image_path, order in (
        ("snowboard-drift-156", "img/snowboard1.jpg", 1),
        ("narty-alpine-172", "img/narty.jpg", 2),
    ):
        Product.objects.using(schema_editor.connection.alias).filter(
            slug=slug, image_path="", featured_order__isnull=True,
        ).update(image_path=image_path, featured_order=order)


class Migration(migrations.Migration):
    dependencies = [("catalog", "0002_product_featured_order_product_image_path")]
    operations = [migrations.RunPython(feature_demo_products, migrations.RunPython.noop)]
