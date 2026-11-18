import re
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Order, PICKUP_CHOICES


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label=_("Imię"), max_length=150, widget=forms.TextInput(attrs={"autocomplete": "given-name"}))
    last_name = forms.CharField(label=_("Nazwisko"), max_length=150, widget=forms.TextInput(attrs={"autocomplete": "family-name"}))
    email = forms.EmailField(label=_("Adres e-mail"), widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    phone = forms.CharField(label=_("Numer telefonu"), max_length=25, widget=forms.TextInput(attrs={"autocomplete": "tel", "type": "tel"}))
    delivery_method = forms.ChoiceField(label=_("Sposób dostawy"), choices=Order.Delivery.choices, initial=Order.Delivery.PICKUP, widget=forms.RadioSelect)
    pickup_location = forms.ChoiceField(label=_("Sklep odbioru"), choices=PICKUP_CHOICES, required=False, initial="gliwice")
    street_address = forms.CharField(label=_("Ulica i numer domu / mieszkania"), max_length=200, required=False, widget=forms.TextInput(attrs={"autocomplete": "address-line1"}))
    postal_code = forms.CharField(label=_("Kod pocztowy"), max_length=6, required=False, widget=forms.TextInput(attrs={"autocomplete": "postal-code", "placeholder": "00-000"}))
    city = forms.CharField(label=_("Miejscowość"), max_length=100, required=False, widget=forms.TextInput(attrs={"autocomplete": "address-level2"}))
    notes = forms.CharField(label=_("Uwagi do zamówienia"), max_length=1000, required=False, widget=forms.Textarea(attrs={"rows": 3}))
    accept_demo = forms.BooleanField(label=_("Potwierdzam zamówienie demonstracyjne."))
    quote = forms.CharField(widget=forms.HiddenInput, max_length=16000)

    def clean_phone(self):
        value = self.cleaned_data["phone"]
        if not re.fullmatch(r"\+?[0-9][0-9 ()-]*[0-9]", value) or not 7 <= sum(c.isdigit() for c in value) <= 15:
            raise forms.ValidationError(_("Podaj prawidłowy numer telefonu."))
        return value

    def clean(self):
        data = super().clean()
        if data.get("delivery_method") == Order.Delivery.COURIER:
            for field in ("street_address", "postal_code", "city"):
                if not data.get(field):
                    self.add_error(field, _("Uzupełnij adres dostawy."))
            if data.get("postal_code") and not re.fullmatch(r"[0-9]{2}-[0-9]{3}", data["postal_code"]):
                self.add_error("postal_code", _("Wpisz kod pocztowy w formacie 00-000."))
            data["pickup_location"] = ""
        elif data.get("delivery_method") == Order.Delivery.PICKUP:
            if not data.get("pickup_location"):
                self.add_error("pickup_location", _("Wybierz sklep odbioru."))
            for field in ("street_address", "postal_code", "city"):
                data[field] = ""
        return data
