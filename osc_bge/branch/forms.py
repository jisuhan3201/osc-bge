from django import forms
from . import models


class BgeResourceForm(forms.ModelForm):

    class Meta:
        model = models.BgeResource
        fields = ('file',)
