from django import forms
from . import models


class FileboxForm(forms.ModelForm):

    class Meta:
        model = models.FormalityFile
        fields = ('file_source',)
