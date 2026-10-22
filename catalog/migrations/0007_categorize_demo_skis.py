from django.db import migrations


def categorize_demo_skis(apps, schema_editor):
    # Tylko znana oferta demo z opisem nart trasowych; nie klasyfikujemy innych produktów.
    apps.get_model("catalog", "Product").objects.using(schema_editor.connection.alias).filter(
        slug="narty-alpine-172", category="skis", ski_subcategory="",
        description__startswith="Wszechstronne narty trasowe",
    ).update(ski_subcategory="downhill")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0006_product_ski_subcategory_and_more")]
    operations = [migrations.RunPython(categorize_demo_skis, migrations.RunPython.noop)]
