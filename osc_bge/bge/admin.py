from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.BgeBranch)
class BgeBranchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "country",
        "state",
        "address",
    )
