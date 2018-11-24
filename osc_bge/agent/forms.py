from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms
from osc_bge.form import models as form_models

class FormalityForm(forms.Form):
    Date = forms.DateField(
        required=False,
        widget=DatePickerInput(format="%Y-%m-%d")
    )

class DateTimeForm(forms.ModelForm):
    class Meta:
        model =form_models.SchoolFormality
        fields = ['school_interview_date', 'school_interview_time']
        widgets = {
            'school_interview_date': DatePickerInput(format="%Y-%m-%d"),
            'school_interview_time': TimePickerInput()
        }

class CancelEnrolmentForm(forms.ModelForm):
    class Meta:
        model =form_models.SchoolFormality
        fields = ['cancel_enrolment_date', 'cancel_enrolment_time']
        widgets = {
            'cancel_enrolment_date': DatePickerInput(format="%Y-%m-%d"),
            'cancel_enrolment_time': TimePickerInput()
        }

class VisaReserveSchedulingForm(forms.ModelForm):

    class Meta:
        model = form_models.Formality
        fields = ['visa_reserve_date', 'visa_reserve_time']
        widgets = {
            'visa_reserve_date': DatePickerInput(format="%Y-%m-%d"),
            'visa_reserve_time': TimePickerInput()
        }

class VisaGrantedForm(forms.ModelForm):

    class Meta:
        model = form_models.Formality
        fields = ['visa_granted_date', 'visa_granted_time']
        widgets = {
            'visa_granted_date': DatePickerInput(format="%Y-%m-%d"),
            'visa_granted_time':TimePickerInput()
        }

class VisaRejectedForm(forms.ModelForm):

    class Meta:
        model = form_models.Formality
        fields = ['visa_rejected_date', 'visa_rejected_time']
        widgets = {
            'visa_rejected_date': DatePickerInput(format="%Y-%m-%d"),
            'visa_rejected_time': TimePickerInput()
        }

class FlightDepartureForm(forms.ModelForm):

    class Meta:
        model = form_models.Formality
        fields = ['air_departure_date', 'air_departure_time']
        widgets = {
            'air_departure_date': DatePickerInput(format="%Y-%m-%d"),
            'air_departure_time': TimePickerInput(),
        }

class FlightArriveForm(forms.ModelForm):

    class Meta:
        model = form_models.Formality
        fields = ['air_arrive_date', 'air_arrive_time']
        widgets = {
            'air_arrive_date': DatePickerInput(format="%Y-%m-%d"),
            'air_arrive_time': TimePickerInput(),
        }

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
        required=False,
        widget=forms.TextInput(attrs={
            'class': "FileButton",
            'type': 'file',
        })
    )

FileFormset = forms.formset_factory(FileForm, extra=1)
