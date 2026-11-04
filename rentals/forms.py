from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class RentalDatesForm(forms.Form):
    start_date = forms.DateField(label=_("Data odbioru"), input_formats=["%Y-%m-%d"], widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    end_date = forms.DateField(label=_("Data zwrotu"), input_formats=["%Y-%m-%d"], widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["min"] = timezone.localdate().isoformat()

    def clean(self):
        data = super().clean()
        start, end = data.get("start_date"), data.get("end_date")
        if start and start < timezone.localdate():
            self.add_error("start_date", _("Data odbioru nie może być w przeszłości."))
        if start and end and end < start:
            self.add_error("end_date", _("Data zwrotu nie może być wcześniejsza niż data odbioru."))
        return data
