from django import forms
from . import models


class SchoolImageForm(forms.ModelForm):

    class Meta:
        model = models.School
        fields = ('image',)


class SchoolPhotoForm(forms.ModelForm):

    class Meta:
        model = models.SchoolPhotos
        fields = ('photo',)


class SchoolFileForm(forms.ModelForm):

    class Meta:
        model = models.School
        fields = ('school_file',)


class SchoolLogForm(forms.ModelForm):

    class Meta:
        model = models.SchoolCommunicationLog
        fields = ('file',)
