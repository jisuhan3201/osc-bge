from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.BgeBranch)
class BgeBranchAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        "name",
        "country",
        "state",
        "address",
    )


@admin.register(models.BgeVideo)
class BgeVideoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'video',
    )
