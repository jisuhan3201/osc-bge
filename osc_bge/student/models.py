from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.school import models as school_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class ParentInfo(TimeStampedModel):

    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(null=True, max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    wechat = models.CharField(null=True, max_length=255, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Student(TimeStampedModel):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    STATUS_CHOICES = (
        ('unregistered', 'Unregistered'),
        ('registered', 'Registered'),
        ('transferred', 'Transferred'),
        ('terminated', 'Terminated'),
    )

    agency_admin = models.ForeignKey(user_models.AgencyAdminUser, on_delete=models.SET_NULL, null=True)
    counselor = models.ForeignKey(user_models.Counselor, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    parent_info = models.ForeignKey(ParentInfo, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True)
    phone = models.CharField(null=True, max_length=140, blank=True)
    email = models.EmailField(null=True, blank=True)
    skype = models.CharField(max_length=140, null=True, blank=True)
    wechat = models.CharField(null=True, max_length=140, blank=True)
    status = models.CharField(null=True, max_length=80, blank=True, default='unregistered', choices=STATUS_CHOICES)
    nationality = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class StudentHistory(TimeStampedModel):

    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True, related_name='student_history')
    current_grade = models.CharField(max_length=80, null=True, blank=True)
    current_school = models.CharField(max_length=140, null=True, blank=True)
    apply_grade = models.CharField(null=True, max_length=80, blank=True)
    eng_level = models.CharField(max_length=140, null=True, blank=True)
    toefl = models.CharField(max_length=80, null=True, blank=True)
    toefljr = models.CharField(max_length=80, null=True, blank=True)
    gpa = models.CharField(max_length=80, null=True, blank=True)
    sat = models.CharField(max_length=80, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.student, self.gpa)


class StudentReport(TimeStampedModel):

    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='report')
    counselor = models.ForeignKey(user_models.Counselor, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    reported_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.id)


class CurrentStudentReview(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    student = models.CharField(max_length=80, null=True, blank=True)
    grade = models.CharField(max_length=80, null=True, blank=True)
    homecity = models.CharField(max_length=80, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class GraduateStudentReview(TimeStampedModel):

    school = models.ForeignKey(school_models.School, on_delete=models.SET_NULL, null=True)
    student = models.CharField(max_length=80, null=True, blank=True)
    attended = models.CharField(max_length=80, null=True, blank=True)
    init_eng = models.CharField(max_length=80, null=True, blank=True)
    gpa_china = models.CharField(max_length=80, null=True, blank=True)
    toefl = models.CharField(max_length=80, null=True, blank=True)
    gpa = models.CharField(max_length=80, null=True, blank=True)
    sat_act = models.CharField(max_length=80, null=True, blank=True)
    activities = models.CharField(max_length=80, null=True, blank=True)
    college = models.CharField(max_length=80, null=True, blank=True)
    major = models.CharField(max_length=80, null=True, blank=True)
