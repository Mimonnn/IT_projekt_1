from django.db import migrations


def categorize_helmet(apps, schema_editor):
    apps.get_model("catalog", "Product").objects.using(schema_editor.connection.alias).filter(
        slug="kask-ridge-m", category="accessories",
    ).update(category="helmets")


def restore_category(apps, schema_editor):
    apps.get_model("catalog", "Product").objects.using(schema_editor.connection.alias).filter(
        slug="kask-ridge-m", category="helmets",
    ).update(category="accessories")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0004_alter_product_category")]
    operations = [migrations.RunPython(categorize_helmet, restore_category)]
