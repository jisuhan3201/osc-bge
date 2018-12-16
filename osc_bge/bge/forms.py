from django import forms
from osc_bge.student import models as student_models


class AccountingForm(forms.ModelForm):

    class Meta:
        model = student_models.StudentAccounting
        fields = ('invoice',)
