from django.utils.translation import gettext_lazy as _
import json
from django.core.serializers.json import DjangoJSONEncoder

from django import forms

from .models import Product
from .taxonomy import SUBCATEGORIES


class ProductAdminForm(forms.ModelForm):
    discount_percent = forms.IntegerField(label=_("Rabat (%)"), required=False, min_value=0, max_value=99, help_text=_("0 lub puste pole wyłącza promocję. Rabat od ceny regularnej."))

    def clean_discount_percent(self):
        if self.add_prefix("discount_percent") not in self.data:
            return self.instance.discount_percent
        return self.cleaned_data["discount_percent"] or 0

    subcategory = forms.ChoiceField(
        label=_("Podkategoria"), required=False,
        help_text=_("Wybierz typ właściwy dla kategorii produktu."),
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
        self.fields["subcategory"].widget.attrs["data-subcategories"] = json.dumps(SUBCATEGORIES, ensure_ascii=False, cls=DjangoJSONEncoder)
