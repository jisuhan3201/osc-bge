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
        "agency_admin",
        "counseler",
        "school",
        "parent_info",
        "name",
        "gender",
        "birthday",
        "image",
        "phone",
        "email",
        "skype",
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
