import datetime
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from osc_bge.agent import models as agent_models
from osc_bge.bge import models as bge_models


def set_filename_format(now, instance, filename):
    """ file format setting e.g)
    {username}-{date}-{microsecond}{extension}
    username-2016-07-12-158859.png """

    return "{username}-{date}-{microsecond}{extension}".format(
        username=instance.username,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
        )

def user_directory_path(instance, filename):
    """
    image upload directory setting e.g)
    images/{year}/{month}/{day}/{username}/{filename}
    images/2016/7/12/username/username-2016-07-12-158859.png
    """
    now = datetime.datetime.now()
    path = "images/{year}/{month}/{day}/{username}/{filename}".format(
        year=now.year,
        month=now.month,
        day=now.day,
        username=instance.username,
        filename=set_filename_format(now, instance, filename),
    )
    return path


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    USER_TYPE = (
        ('bge_admin', "BGE_Admin"),
        ('bge_team', 'BGE_Team'),
        ('bge_branch_admin', "BGE_Branch_Admin"),
        ('bge_accountant', 'BGE_Accountant'),
        ('agency_admin', 'Agency_Admin'),
        ('agency_branch_admin', 'Agency_Branch_Admin'),
        ('counselor', 'Counselor'),
    )

    address = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    type = models.CharField(max_length=140, null=True, choices=USER_TYPE, blank=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.username)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

# Bge admission team
class BgeAdminUser(models.Model):

    PARTITION_CHOICES = (
        ('entrance', 'ENTRANCE'),
        ('accounting', 'ACCOUNTING'),
        ('admin', 'ADMIN'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    group = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True)
    partition = models.CharField(max_length=255, choices=PARTITION_CHOICES, null=True)

    def __str__(self):
        return "{}".format(self.user)

# Bge branch manager
class BgeBranchAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='branch_admin')
    branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True, related_name='branch_admin')

    def __str__(self):
        return "{}".format(self.user)

# Bge branch coordi
class BgeBranchCoordinator(models.Model):

    POSITION_CHOICES = (
        ('school_coordi', 'School coordinator'),
        ('student_coordi', 'Student coordinator'),
        ('host_coordi', 'Host coordinator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='coordinator')
    branch = models.ForeignKey(bge_models.BgeBranch, on_delete=models.SET_NULL, null=True, related_name='branch_coordi')
    position = models.CharField(max_length=255, choices=POSITION_CHOICES, null=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.branch)


class AgencyHeadAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="agency_head_admin")
    agency_head = models.ForeignKey(agent_models.AgencyHead, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.agency_head, self.user)


class AgencyAdminUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="agency_admin")
    agency = models.ForeignKey(agent_models.Agency, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} - {}".format(self.agency, self.user)


class Counselor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="counselor")
    agency = models.ForeignKey(agent_models.Agency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user)
