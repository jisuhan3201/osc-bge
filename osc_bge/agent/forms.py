from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from osc_bge.form import models as form_models


class FormalityForm(forms.Form):
    Date = forms.DateField(
        widget=DatePickerInput(format="%Y-%m-%d")
    )
