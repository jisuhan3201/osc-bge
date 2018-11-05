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
    birthday = models.DateField(null=True)
    country = CountryField(null=True)
    image = models.ImageField(upload_to='images')
    phone = models.CharField(null=True, max_length=255)
    email = models.EmailField(null=True)
    wechat = models.CharField(null=True, max_length=255)
    skype = models.CharField(null=True, max_length=255)
    major = models.CharField(null=True, max_length=255)
    grade = models.CharField(null=True, max_length=255)
    status = models.CharField(null=True, max_length=255)

    def __str__(self):
        return "{}".format(self.name)


class StudentHistory(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    is_school_active = models.BooleanField()
    ibt = models.IntegerField(null=True)
    gpa = models.IntegerField(null=True)
    sat = models.IntegerField(null=True)
    abroad_year = models.DateField(null=True)
    past_eng = models.TextField(null=True)
    past_gpa = models.IntegerField(null=True)
    is_deleted = models.BooleanField()

    def __str__(self):
        return "{} - {}".format(self.student, self.gpa)
