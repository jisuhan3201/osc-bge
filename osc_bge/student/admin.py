from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "coordinator",
        "agency_admin",
        "agency_branch_admin",
        "counseler",
        "school",
        "host",
        "parent",
        "name",
        "gender",
        "birthday",
        "country",
        "image",
        "phone",
        "email",
        "wechat",
        "skype",
        "major",
        "grade",
        "status",
    )

@admin.register(models.StudentHistory)
class StudentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "school",
        "is_school_active",
        "ibt",
        "gpa",
        "sat",
        "abroad_year",
        "past_eng",
        "past_gpa",
        "is_deleted",
    )
