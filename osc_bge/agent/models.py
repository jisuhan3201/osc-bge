from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Agency(TimeStampedModel):

    name = models.CharField(max_length=140, null=True, blank=True)
    branch = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.name, self.branch)


# class AgencyBranch(TimeStampedModel):
#
#     agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=255, null=True)
#     country = CountryField(null=True)
#     state = models.CharField(max_length=255, null=True)
#     address = models.CharField(max_length=255, null=True)
#     students = models.IntegerField(null=True)
#
#     def __str__(self):
#         return "{}".format(self.name)
