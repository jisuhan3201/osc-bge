from django import forms
from . import models

class StudentImageForm(forms.ModelForm):

    class Meta:
        model = models.Student
        fields = ('image',)
