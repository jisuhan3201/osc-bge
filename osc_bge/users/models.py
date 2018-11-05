from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from osc_bge.agent import models as agent_models
from osc_bge.bge import models as bge_models


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    GROUP_CHOICES = (
        ('bge', 'BGE'),
        ('agency', 'AGENCY'),
        ('other', 'Other'),
    )
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    country = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    group = models.CharField(max_length=255, choices=GROUP_CHOICES, null=True)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class BgeAdminUser(models.Model):

    PARTITION_CHOICES = (
        ('entrance', 'ENTRANCE'),
        ('accounting', 'ACCOUNTING'),
        ('admin', 'ADMIN'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    partition = models.CharField(max_length=255, choices=PARTITION_CHOICES, null=True)

    def __str__(self):
        return "{}".format(self.user)


class BgeBranchAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bge = models.ForeignKey(BgeAdminUser, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{}".format(self.user)


class BgeBranchCoordinator(models.Model):

    POSITION_CHOICES = (
        ('student_admin', 'STUDENT_ADMIN'),
        ('school_admin', 'SCHOOL_ADMIN'),
        ('host_admin', 'HOST_ADMIN'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    branch_admin = models.ForeignKey(BgeBranchAdminUser, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=255, choices=POSITION_CHOICES, null=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.branch)


class AgencyAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    agency = models.ForeignKey(agent_models.Agency, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.agency, self.user)


class AgencyBranchAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    agench_branch = models.ForeignKey(agent_models.AgencyBranch, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.agency_branch, self.user)

class Counseler(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    coordinator = models.ForeignKey(BgeBranchCoordinator, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(AgencyAdminUser, on_delete=models.SET_NULL, null=True)
    agency_branch = models.ForeignKey(AgencyBranchAdminUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.user)


class Host(models.Model):

    ACTIVE_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    coordinator = models.ForeignKey(BgeBranchCoordinator, on_delete=models.SET_NULL, null=True)
    active_status = models.CharField(max_length=255, choices=ACTIVE_STATUS, null=True)
    phone = models.CharField(null=True, max_length=255)
    status = models.CharField(null=True, max_length=255)
    school = models.CharField(null=True, max_length=255)
    job = models.CharField(null=True, max_length=255)
    employer = models.CharField(null=True, max_length=255)
    is_married = models.BooleanField()
    children = models.IntegerField(null=True)
    pet = models.BooleanField()
    plan = models.TextField(null=True)
    gender_hope = models.CharField(null=True, choices=GENDER_CHOICES, max_length=255)
    student_available = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    filename = models.FileField(upload_to="host", null=True)
    is_deleted = models.BooleanField()

    def __str__(self):
        return "{}".format(self.user)


class Parent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_deleted = models.BooleanField()

    def __str__(self):
        return "{}".format(self.user)
