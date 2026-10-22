from django.db import migrations


def categorize_demo_snowboard(apps, schema_editor):
    apps.get_model("catalog", "Product").objects.using(schema_editor.connection.alias).filter(
        slug="snowboard-drift-156", category="snowboards", subcategory="",
        description__startswith="Snowboard all-mountain",
    ).update(subcategory="all_mountain")


class Migration(migrations.Migration):
    dependencies = [("catalog", "0008_remove_product_product_ski_subcategory_valid_and_more")]
    operations = [migrations.RunPython(categorize_demo_snowboard, migrations.RunPython.noop)]
