from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "state",
        "address",
        "program",
    )

@admin.register(models.AgencyBranch)
class AgencyBranchAdmin(admin.ModelAdmin):

    list_display = (
        "agency",
        "name",
        "country",
        "state",
        "address",
        "students",
    )