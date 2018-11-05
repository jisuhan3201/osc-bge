from django.db import models
from osc_bge.users import models as user_models
from osc_bge.student import models as student_models
from osc_bge.school import models as school_models
from django_countries.fields import CountryField

# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


# Notdone
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
    types = models.CharField(max_length=255, null=True)
    content = models.TextField(null=True)
    priority = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{}".format(self.title)
