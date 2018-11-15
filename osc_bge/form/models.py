from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.student import models as student_models
from osc_bge.school import models as school_models


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

    counseler = models.ForeignKey(user_models.Counseler, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
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

    counsel = models.OneToOneField(Counsel, on_delete=models.SET_NULL, null=True)
    payment_complete = models.NullBooleanField(blank=True)
    apply_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    visa_reserve_at = models.DateTimeField(null=True, blank=True)
    visa_approve_at = models.DateTimeField(null=True, blank=True)
    visa_denied_at = models.DateTimeField(null=True, blank=True)
    departure_ot_at = models.DateTimeField(null=True, blank=True)
    departure_complete = models.NullBooleanField(blank=True)
    air_ticketing_at = models.DateTimeField(null=True, blank=True)
    air_departure_at = models.DateTimeField(null=True, blank=True)
    air_arrive_at = models.DateTimeField(null=True, blank=True)
    air_departure_port = models.CharField(max_length=255, null=True, blank=True)
    air_arrive_port = models.CharField(max_length=255, null=True, blank=True)
    pickup_num = models.IntegerField(null=True, blank=True)
    pickup_at = models.DateTimeField(null=True, blank=True)
    is_pet = models.NullBooleanField(blank=True)
    is_child = models.NullBooleanField(blank=True)
    is_allergy = models.NullBooleanField(blank=True)

    def __str__(self):
        return "{}".format(self.id)


class SchoolFormality(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    formality = models.ForeignKey(Formality, on_delete=models.SET_NULL, null=True, related_name="school_formality")
    school_priority = models.SmallIntegerField(null=True, blank=True)
    class_start_at = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=80, null=True, blank=True)
    form_apply_fee = models.NullBooleanField(blank=True)
    entrance_grade = models.CharField(null=True, max_length=255)
    entrance_fee = models.IntegerField(null=True)
    entrance_prefee = models.IntegerField(null=True)
    entrance_restfee = models.IntegerField(null=True)
    interview_reserve_at = models.DateTimeField(null=True)
    training_reserve_at = models.DateTimeField(null=True)
    entrance_approve_at = models.DateTimeField(null=True)
    entrance_canceled_at = models.DateTimeField(null=True)
    i20_apply_at = models.DateTimeField(null=True)
    i20_fee = models.IntegerField(null=True)
    i20_prefee = models.IntegerField(null=True)
    i20_restfee = models.IntegerField(null=True)
    i20_receive_at = models.DateTimeField(null=True)
    program_fee_complete = models.NullBooleanField(blank=True)
    program_fee_send_at = models.DateTimeField(null=True)
    program_fee = models.IntegerField(null=True)
    program_prefee = models.IntegerField(null=True)
    program_restfee = models.IntegerField(null=True)

    def __str__(self):
        return "{}".format(self.id)
