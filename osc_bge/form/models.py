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

    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
    memo = models.ForeignKey(Memo, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="form", null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(null=True, max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    wechat = models.CharField(null=True, max_length=255, blank=True)
    skype = models.CharField(null=True, max_length=255, blank=True)
    school = models.CharField(null=True, max_length=255, blank=True)
    grade = models.CharField(null=True, max_length=255, blank=True)
    program = models.CharField(null=True, max_length=255, blank=True)
    apply_country = CountryField(null=True, blank=True)
    apply_date = models.DateField(null=True, blank=True)
    apply_grade = models.CharField(null=True, max_length=255, blank=True)
    apply_semester = models.CharField(max_length=255, null=True, blank=True)
    apply_possibility = models.IntegerField(null=True, blank=True)
    is_formality = models.BooleanField()
    client_grade = models.CharField(max_length=255, null=True, blank=True)
    gpa = models.IntegerField(null=True, blank=True)
    sat = models.IntegerField(null=True, blank=True)
    ibt = models.IntegerField(null=True, blank=True)
    ibtjr = models.IntegerField(null=True, blank=True)
    eng_level = models.CharField(max_length=255, null=True, blank=True)
    parent_name = models.CharField(max_length=255, null=True, blank=True)
    parent_phone = models.CharField(max_length=255, null=True, blank=True)
    parent_wechat = models.CharField(max_length=255, null=True, blank=True)
    parent_email = models.EmailField(null=True, blank=True)
    desire_state = models.CharField(max_length=255, null=True, blank=True)
    desire_student = models.IntegerField(null=True, blank=True)
    desire_grade = models.CharField(max_length=255, null=True, blank=True)
    desire_types = models.CharField(max_length=255, choices=SCHOOL_TYPE, null=True, blank=True)
    desire_is_boarding = models.BooleanField()
    desire_is_communting = models.BooleanField()
    desire_ibt = models.IntegerField(null=True, blank=True)
    desire_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    first_date = models.DateTimeField(null=True, blank=True)
    second_date = models.DateTimeField(null=True, blank=True)
    third_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)


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

    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, blank=True)
    memo = models.ForeignKey(Memo, on_delete=models.SET_NULL, null=True, blank=True)
    counsel_at = models.DateTimeField(null=True)
    payment_complete = models.BooleanField()
    apply_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)
    visa_reserve_at = models.DateTimeField(null=True)
    visa_approve_at = models.DateTimeField(null=True)
    visa_denied_at = models.DateTimeField(null=True)
    departure_ot_at = models.DateTimeField(null=True)
    departure_complete = models.BooleanField()
    air_ticketing_at = models.DateTimeField(null=True)
    air_departure_at = models.DateTimeField(null=True)
    air_arrive_at = models.DateTimeField(null=True)
    air_departure_port = models.CharField(max_length=255, null=True)
    air_arrive_port = models.CharField(max_length=255, null=True)
    pickup_num = models.IntegerField(null=True)
    pickup_at = models.DateTimeField(null=True)
    is_pet = models.BooleanField()
    is_child = models.BooleanField()
    is_allergy = models.BooleanField()

    def __str__(self):
        return "{}".format(self.id)


class SchoolFormality(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    formality = models.ForeignKey(Formality, on_delete=models.SET_NULL, null=True)
    form_apply_fee = models.BooleanField()
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
    program_fee_complete = models.BooleanField()
    program_fee_send_at = models.DateTimeField(null=True)
    program_fee = models.IntegerField(null=True)
    program_prefee = models.IntegerField(null=True)
    program_restfee = models.IntegerField(null=True)

    def __str__(self):
        return "{}".format(self.id)
