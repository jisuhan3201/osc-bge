from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.ParentInfo)
class ParentInfoAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "wechat",
    )

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "coordinator",
        "agency_admin",
        "agency_branch_admin",
        "counseler",
        "school",
        "host",
        "parent_info",
        "name",
        "gender",
        "birthday",
        "image",
        "phone",
        "email",
        "wechat",
        "status",
    )

@admin.register(models.StudentHistory)
class StudentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "current_grade",
        "current_school",
        "apply_grade",
        "eng_level",
        "toefl",
        "toefljr",
        "gpa",
        "sat",
        "address"
    )
