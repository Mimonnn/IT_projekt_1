import json

from django import forms

from .models import Product
from .taxonomy import SUBCATEGORIES


class ProductAdminForm(forms.ModelForm):
    subcategory = forms.ChoiceField(
        label="Podkategoria", required=False,
        help_text="Wybierz typ właściwy dla kategorii produktu.",
    )

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.data.get(self.add_prefix("category")) if self.is_bound else (
            self.initial.get("category", self.instance.category)
        )
        choices = SUBCATEGORIES.get(category, [])
        self.fields["subcategory"].choices = [("", "---------"), *choices]
        self.fields["subcategory"].widget.attrs["data-subcategories"] = json.dumps(SUBCATEGORIES, ensure_ascii=False)
