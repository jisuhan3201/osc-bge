from django.db import models
from django_countries.fields import CountryField
from osc_bge.users import models as user_models
from osc_bge.agent import models as agent_models

class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class BgeBranch(TimeStampedModel):

    name = models.CharField(max_length=255, null=True)
    country = CountryField(null=True)
    state = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{}".format(self.name)


class BgeVideo(TimeStampedModel):

    video = models.FileField(upload_to='videos/', null=True, blank=True)
