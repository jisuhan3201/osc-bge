from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.HostFamily)
class HostFamilyAdmin(admin.ModelAdmin):

    list_display = (
        "host_coordi",
        "provider_branch",
        "name",
        "status",
        "address",
        "phone",
        "email",
        "possible_school",
        "occupation",
        "employer",
        "marital_status",
        "children",
        "pets",
        "student_preference",
        "hosting_capacity",
        "starting_date",
        "last_update_date",
        "comment",
        "provider",
    )


@admin.register(models.HostStudent)
class HostStudentAdmin(admin.ModelAdmin):

    list_display = (
        "host",
        "student",
        "next_year_plan",
    )


@admin.register(models.CommunicationLog)
class CommunicationLogAdmin(admin.ModelAdmin):

    list_display = (
        "host",
        "writer",
        "date",
        "category",
        "priority",
        "comment",
    )

@admin.register(models.HostStudentReport)
class HostStudentReportAdmin(admin.ModelAdmin):

    list_display = (
        "host_coordi",
        "host",
        "student",
        "description",
        "rate",
        "improvement",
        "cultural_fluency",
        "house_rule_attitude",
        "responsibility",
        "communication",
        "sleeping_habits",
        "school_attendance",
        "comment",
        "status",
        "submitted_date",
        "due_date",
    )
