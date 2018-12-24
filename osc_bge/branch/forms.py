from django import forms
from . import models


class BgeResourceForm(forms.ModelForm):

    class Meta:
        model = models.BgeResource
        fields = ('file',)


class HostStudentPhotoForm(forms.ModelForm):

    class Meta:
        model = models.ReportPhoto
        fields = ('photo',)

class HostStudentFileForm(forms.ModelForm):

    class Meta:
        model = models.ReportFile
        fields = ('file',)
