from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.bge import models as bge_models
from osc_bge.student import models as student_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class HostFamily(TimeStampedModel):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospective', 'Prospective'),
    )
    PREFERENCE_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    host_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True, related_name='host')
    provider_branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=80, null=True, blank=True, choices=STATUS_CHOICES)
    address = models.CharField(max_length=140, null=True, blank=True)
    phone = models.CharField(max_length=80, null=True, blank=True)
    email = models.CharField(max_length=140, null=True, blank=True)
    possible_school = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=140, null=True, blank=True)
    employer = models.CharField(max_length=80, null=True, blank=True)
    marital_status = models.CharField(max_length=80, null=True, blank=True)
    children = models.CharField(max_length=80, null=True, blank=True)
    pets = models.CharField(max_length=80, null=True, blank=True)
    student_preference = models.CharField(max_length=80, null=True, blank=True, choices=PREFERENCE_CHOICES)
    hosting_capacity = models.CharField(max_length=80, null=True, blank=True)
    starting_date = models.DateField(null=True, blank=True)
    last_update_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    provider = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class HostStudent(TimeStampedModel):

    PLAN_CHOICES = (
        ('same_student', 'Same-Student'),
        ('change_student', 'Change-student'),
        ('na', 'N/A'),
        ('a', 'A')
    )

    host = models.ForeignKey(HostFamily, on_delete=models.CASCADE, null=True, related_name='students')
    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, related_name="host")
    next_year_plan = models.CharField(max_length=140, null=True, blank=True, choices=PLAN_CHOICES)
    communication_log = models.TextField(null=True, blank=True)


class HostPhoto(TimeStampedModel):

    host = models.OneToOneField(HostFamily, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='images', null=True, blank=True)


class HostFile(TimeStampedModel):

    host = models.OneToOneField(HostFamily, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='files', null=True, blank=True)


class CommunicationLog(TimeStampedModel):

    host = models.ForeignKey(HostFamily, on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(user_models.User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=80, null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class HostStudentReport(TimeStampedModel):

    STATUS_CHOICES = (
        ('incomplete', 'Incomplete'),
        ('complete', 'complete'),
        ('submitted', 'Submitted'),
    )

    host_coordi = models.ForeignKey(user_models.BgeBranchCoordinator, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(HostFamily, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(student_models.Student, on_delete=models.SET_NULL, null=True, related_name='host_report')
    description = models.TextField(null=True, blank=True)
    rate = models.CharField(max_length=80, null=True, blank=True)
    improvement = models.CharField(max_length=80, null=True, blank=True)
    cultural_fluency = models.TextField(null=True, blank=True)
    house_rule_attitude = models.TextField(null=True, blank=True)
    responsibility = models.TextField(null=True, blank=True)
    communication = models.TextField(null=True, blank=True)
    sleeping_habits = models.TextField(null=True, blank=True)
    school_attendance = models.TextField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=80, null=True, blank=True, choices=STATUS_CHOICES)
    submitted_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)


class ReportPhoto(TimeStampedModel):

    report = models.ForeignKey(HostStudentReport, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='image', null=True, blank=True)


class ReportFile(TimeStampedModel):

    report = models.ForeignKey(HostStudentReport, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='file', null=True, blank=True)
