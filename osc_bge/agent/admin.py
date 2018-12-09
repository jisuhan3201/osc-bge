from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.AgencyHead)
class AgencyHeadAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "location",
        "number_branches",
        "capacity_students",
        "commission",
        "promotion",
        "others",
        "comment",
    )


@admin.register(models.Agency)
class AgencyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "head",
        "name",
        "location",
        "capacity_students",
        "commission",
        "promotion",
        "others",
        "comment",
    )

@admin.register(models.AgencyProgram)
class AgencyProgramAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'head',
        'program'
    )


@admin.register(models.AgencyHeadContactInfo)
class AgencyHeadContactInfoAdmin(admin.ModelAdmin):

    list_display = (
        "agent",
        "name",
        "contracted_date",
        "phone",
        "email",
        "skype",
        "wechat",
        "location",
        "level",
        "image",
    )

@admin.register(models.AgencyBranchProgram)
class AgencyBranchProgramAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'branch',
        'program'
    )


@admin.register(models.AgentRelationshipHistory)
class AgentRelationshipHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "head",
        "writer",
        "name",
        "date",
        "location",
        "category",
        "priority",
        "comment",
    )
