from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.school import models as school_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Student(TimeStampedModel):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    coordinator = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True)
    agency_admin = models.ForeignKey(user_models.AgencyAdminUser, on_delete=models.SET_NULL, null=True)
    agency_branch_admin = models.ForeignKey(user_models.AgencyBranchAdminUser, on_delete=models.SET_NULL, null=True)
    counseler = models.ForeignKey(user_models.Counseler, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(user_models.Host, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey(user_models.Parent, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    phone = models.CharField(null=True, max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    wechat = models.CharField(null=True, max_length=255, blank=True)
    skype = models.CharField(null=True, max_length=255, blank=True)
    major = models.CharField(null=True, max_length=255, blank=True)
    grade = models.CharField(null=True, max_length=255, blank=True)
    status = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class StudentHistory(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    is_school_active = models.BooleanField()
    ibt = models.IntegerField(null=True, blank=True)
    gpa = models.IntegerField(null=True, blank=True)
    sat = models.IntegerField(null=True, blank=True)
    abroad_year = models.DateField(null=True, blank=True)
    past_eng = models.TextField(null=True, blank=True)
    past_gpa = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField()

    def __str__(self):
        return "{} - {}".format(self.student, self.gpa)
