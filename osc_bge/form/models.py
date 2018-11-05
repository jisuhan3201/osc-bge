from django.db import models
from osc_bge.report import models as report_models

# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

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

    student = models.ForeignKey(student_models.Student, on_delete=SET_NULL, null=True, blank=True)
    memo = models.ForeignKey(report_models.Memo, on_delete=SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="form", null=True)
    client = models.CharField(max_length=255, null=True)
    country = CountryField(null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(null=True, max_length=255)
    email = models.EmailField(null=True)
    wechat = models.CharField(null=True, max_length=255)
    skype = models.CharField(null=True, max_length=255)
    school = models.CharField(null=True, max_length=255)
    grade = models.CharField(null=True, max_length=255)
    program = models.CharField(null=True, max_length=255)
    apply_country = CountryField(null=True)
    apply_date = models.DateField(null=True)
    apply_grade = models.CharField(null=True, max_length=255)
    apply_semester = models.CharField(max_length=255, null=True)
    apply_possibility = models.IntegerField(null=True)
    is_formality = models.BooleanField(null=True)
    client_grade = models.CharField(max_length=255, null=True)
    gpa = models.IntegerField(null=True)
    sat = models.IntegerField(null=True)
    ibt = models.IntegerField(null=True)
    ibtjr = models.IntegerField(null=True)
    eng_level = models.CharField(max_length=255, null=True)
    parent_name = models.CharField(max_length=255, null=True)
    parent_phone = models.CharField(max_length=255, null=True)
    parent_wechat = models.CharField(max_length=255, null=True)
    parent_email = models.EmailField(null=True)
    desire_state = models.CharField(max_length=255, null=True)
    desire_student = models.IntegerField(null=True)
    desire_grade = models.CharField(max_length=255, null=True)
    desire_types = models.CharField(max_length=255, choices=SCHOOL_TYPE, null=True)
    desire_is_boarding = models.BooleanField(null=True)
    desire_is_communting = models.BooleanField(null=True)
    desire_ibt = models.IntegerField(null=True)
    desire_fee = models.DecimalField(max_digits=10, decimal_places=2)
    first_date = models.DateTimeField(null=True)
    second_date = models.DateTimeField(null=True)
    third_date = models.DateTimeField(null=True)

    def __str__(self):
        return "{}".format(self.id)
