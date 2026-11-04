from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Login"), widget=forms.TextInput(attrs={"autofocus": True, "autocomplete": "username"}))


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        labels = {"username": _("Login")}
        widgets = {"username": forms.TextInput(attrs={"autocomplete": "username", "autofocus": True})}


class CartQuantityForm(forms.Form):
    quantity = forms.IntegerField(label=_("Ilość"), min_value=1, max_value=2147483647)


class ProfileForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if phone and not 7 <= sum(character.isdigit() for character in phone) <= 15:
            raise forms.ValidationError(_("Numer telefonu musi zawierać od 7 do 15 cyfr."))
        return phone

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        labels = {"first_name": _("Imię"), "last_name": _("Nazwisko"), "email": _("Adres e-mail"), "phone": _("Numer telefonu")}
        widgets = {
            "first_name": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "type": "tel"}),
        }
