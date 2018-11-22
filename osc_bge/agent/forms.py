from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from osc_bge.form import models as form_models

class FormalityForm(forms.Form):
    Date = forms.DateField(
        widget=DatePickerInput(format="%Y-%m-%d")
    )


# class FileForm(forms.ModelForm):
#     class Meta:
#         model = form_models.FormalityFile
#         fields = ("formality", "name", "file_source", )


class FileForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'TableInnerInput',
            'placeholder': 'File name',
            'style': "width:100%;",
        })
    )
    file_source = forms.FileField(
        label="Choose File",
        label_suffix="",
        widget=forms.TextInput(attrs={
            'class': "FileButton",
            'type': 'file'
        })
    )

FileFormset = forms.formset_factory(FileForm, extra=1)

# FileFormset = forms.modelformset_factory(
#     form_models.FormalityFile,
#     fields=('formality', 'name', 'file_source',),
#     extra=1,
#
#
# )
