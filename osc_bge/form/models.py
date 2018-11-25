from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.student import models as student_models
from osc_bge.school import models as school_models
import datetime
import os


# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Memo(TimeStampedModel):

    bge = models.ForeignKey(user_models.BgeAdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    branch_admin = models.ForeignKey(user_models.BgeBranchAdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    coordinator = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True, blank=True)
    agency_admin = models.ForeignKey(user_models.AgencyAdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    agency_branch_admin = models.ForeignKey(user_models.AgencyBranchAdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    counseler = models.ForeignKey(user_models.Counseler, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True, blank=True)
    host = models.ForeignKey(user_models.Host, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    types = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=255, null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)


class Counsel(TimeStampedModel):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    SCHOOL_TYPE = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('only_male', 'Only-Male'),
        ('only_female', 'Only-Female'),
        ('Coed', 'Coed'),
    )

    counseler = models.ForeignKey(user_models.Counseler, on_delete=models.SET_NULL, null=True, blank=True, related_name="counseling")
    student = models.OneToOneField(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True, related_name="counsel")
    counseling_date = models.DateField(null=True, blank=True)
    desire_country = models.CharField(max_length=80, null=True, blank=True)
    program_interested = models.CharField(null=True, max_length=255, blank=True)
    possibility = models.CharField(max_length=80, null=True, blank=True)
    expected_departure = models.DateField(null=True, blank=True)
    client_class = models.CharField(max_length=80, null=True, blank=True)
    detail = models.TextField(null=True)
    contact_first = models.CharField(max_length=140, null=True, blank=True)
    contact_second = models.CharField(max_length=140, null=True, blank=True)
    contact_third = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        ordering = ['-created_at']


class HomeStay(TimeStampedModel):

    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
    memo = models.ForeignKey(Memo, on_delete=models.SET_NULL, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    culture_adapt = models.IntegerField(null=True, blank=True)
    culture_improve = models.TextField(null=True, blank=True)
    rule_observe = models.IntegerField(null=True, blank=True)
    rule_improve = models.TextField(null=True, blank=True)
    arrange_per = models.IntegerField(null=True, blank=True)
    arrange_improve = models.TextField(null=True, blank=True)
    conversation_per = models.IntegerField(null=True, blank=True)
    conversation_improve = models.TextField(null=True, blank=True)
    timestrict_per = models.IntegerField(null=True, blank=True)
    timestrict_improve = models.TextField(null=True, blank=True)
    class_attendancy = models.IntegerField(null=True, blank=True)
    class_attendancy_improve = models.TextField(null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.student)


class MonthlyReport(TimeStampedModel):

    student_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, related_name="student_coordi", null=True, blank=True)
    school_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, related_name="school_coordi", null=True, blank=True)
    host_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, related_name="host_coordi", null=True, blank=True)
    agency_branch_admin = models.ForeignKey(user_models.AgencyBranchAdminUser, related_name="agency_branch_admin", on_delete=models.SET_NULL, null=True, blank=True)
    counseler = models.ForeignKey(user_models.Counseler, on_delete=models.SET_NULL, related_name="counseler", null=True, blank=True)
    host = models.ForeignKey(user_models.Host, on_delete=models.SET_NULL, related_name="host", null=True, blank=True)
    form_homestay = models.ForeignKey(HomeStay, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
    memo = models.ForeignKey(Memo, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    priority = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    to_parent = models.DateTimeField(null=True)
    to_agency = models.DateTimeField(null=True)
    admin_approve = models.DateTimeField(null=True)
    student_coordi_at = models.DateTimeField(null=True)
    school_coordi_at = models.DateTimeField(null=True)
    host_coordi_at = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    filetype = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{}".format(self.title)


class Formality(TimeStampedModel):

    counsel = models.OneToOneField(Counsel, on_delete=models.SET_NULL, null=True, related_name="formality")
    payment_complete = models.NullBooleanField(blank=True)
    apply_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(null=True, blank=True)
    visa_reserve_date = models.DateField(null=True, blank=True)
    visa_reserve_time = models.TimeField(null=True, blank=True)
    visa_granted_date = models.DateField(null=True, blank=True)
    visa_granted_time = models.TimeField(null=True, blank=True)
    visa_copy_recieved = models.NullBooleanField(blank=True)
    visa_rejected_date = models.DateField(null=True, blank=True)
    visa_rejected_time = models.TimeField(null=True, blank=True)
    eticket_attached = models.NullBooleanField(blank=True)
    air_departure_date = models.DateField(null=True, blank=True)
    air_departure_time = models.TimeField(null=True, blank=True)
    air_departure_port = models.CharField(max_length=140, null=True, blank=True)
    air_arrive_date = models.DateField(null=True, blank=True)
    air_arrive_time = models.TimeField(null=True, blank=True)
    air_arrive_port = models.CharField(max_length=140, null=True, blank=True)
    pickup_num = models.CharField(max_length=80, null=True, blank=True)
    departure_ot = models.DateField(null=True, blank=True)
    departure_confirmed = models.DateField(null=True, blank=True)

    @property
    def school_formality_count(self):
        result = self.school_formality.filter(processing_fee_done=True).count()
        return result

    @property
    def payment_complete_fee(self):
        fees = self.school_formality.filter(processing_fee_done=True)
        result = 0
        for i in fees:
            if i.processing_fee:
                result += i.processing_fee
        return result

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        ordering = ['created_at']


class SchoolFormality(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    formality = models.ForeignKey(Formality, on_delete=models.SET_NULL, null=True, related_name="school_formality")
    school_priority = models.SmallIntegerField(null=True, blank=True)
    class_start_at = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=80, null=True, blank=True)
    processing_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    processing_fee_done = models.NullBooleanField(blank=True)
    enrolment_apply_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    enrolment_apply_done = models.NullBooleanField(blank=True)
    enrolment_apply_done_date = models.DateTimeField(null=True, blank=True)
    prepared_passport = models.NullBooleanField(blank=True)
    prepared_transcript = models.NullBooleanField(blank=True)
    prepared_eng_exams = models.NullBooleanField(blank=True)
    prepared_recommendation = models.NullBooleanField(blank=True)
    prepared_essay = models.NullBooleanField(blank=True)
    school_interview_date = models.DateField(null=True, blank=True)
    school_interview_time = models.TimeField(null=True, blank=True)
    mock_interview = models.NullBooleanField(blank=True)
    school_interview_done = models.NullBooleanField(blank=True)
    acceptance_date = models.DateField(null=True, blank=True)
    acceptance_letter = models.NullBooleanField(blank=True)
    cancel_enrolment_date = models.DateField(null=True, blank=True)
    cancel_enrolment_time = models.TimeField(null=True, blank=True)
    i20_completed = models.NullBooleanField(blank=True)
    i20_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    i20_receipt = models.NullBooleanField(blank=True)
    i20_received_date = models.DateField(null=True, blank=True)
    i20_copy = models.NullBooleanField(blank=True)
    i20_tracking = models.CharField(max_length=255, null=True, blank=True)
    provider_application = models.NullBooleanField(blank=True)
    bge_program_application = models.NullBooleanField(blank=True)
    immunization = models.NullBooleanField(blank=True)
    financial_support = models.NullBooleanField(blank=True)
    program_fee_completed = models.NullBooleanField(blank=True)
    program_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    program_fee_receipt = models.NullBooleanField(blank=True)

    @property
    def payment_amount(self):
        result = self.program_fee - self.i20_fee
        return result

    def __str__(self):
        return "{}".format(self.id)


def set_filename_format(now, instance, filename):

    return "{date}-{microsecond}{extension}".format(
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
        )

def accommodation_directory_path(instance, filename):

    now = datetime.datetime.now()
    path = "accommodation/{year}/{month}/{day}/{filename}".format(
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance, filename),
    )
    return path


class AccommodationFormality(TimeStampedModel):

    HOST_CHOICES = (
        ('a', 'A-Host'),
        ('b', 'B-Host'),
        ('c', 'C-Host'),
    )

    formality = models.OneToOneField(Formality, on_delete=models.SET_NULL, null=True, related_name="accommodation")
    with_animal = models.NullBooleanField(blank=True)
    with_child = models.NullBooleanField(blank=True)
    with_other_student = models.NullBooleanField(blank=True)
    other_preference = models.TextField(null=True, blank=True)
    application_at = models.DateTimeField(null=True, blank=True)
    recommendation_a = models.FileField(upload_to=accommodation_directory_path, null=True, blank=True)
    recommendation_a_comment = models.CharField(max_length=255, null=True, blank=True)
    recommendation_b = models.FileField(upload_to=accommodation_directory_path, null=True, blank=True)
    recommendation_b_comment = models.CharField(max_length=255, null=True, blank=True)
    recommendation_c = models.FileField(upload_to=accommodation_directory_path, null=True, blank=True)
    recommendation_b_comment = models.CharField(max_length=255, null=True, blank=True)
    homestay_recommendation_at = models.DateTimeField(null=True, blank=True)
    host_selection = models.CharField(max_length=140, choices=HOST_CHOICES, null=True, blank=True)
    host_selection_at = models.DateTimeField(null=True, blank=True)
    parent_accommodation_guest_num = models.CharField(max_length=80, null=True, blank=True)
    parent_length_of_stay = models.CharField(max_length=80, null=True, blank=True)
    parent_other_preference = models.TextField(null=True, blank=True)
    parent_accommodation_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)


def file_directory_path(instance, filename):

    now = datetime.datetime.now()
    path = "formality/{year}/{month}/{day}/{filename}".format(
        year=now.year,
        month=now.month,
        day=now.day,
        filename=set_filename_format(now, instance, filename),
    )
    return path


class FormalityFile(TimeStampedModel):

    formality = models.ForeignKey(Formality, on_delete=models.SET_NULL, null=True, related_name="formality_file")
    name = models.CharField(max_length=140, null=True, blank=True)
    file_source = models.FileField(upload_to=file_directory_path, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)
