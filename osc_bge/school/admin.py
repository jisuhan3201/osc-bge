from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "type",
        "image",
        "address",
        "contacts",
        "founded",
        "transfer",
        "term",
        "number_students",
    )

@admin.register(models.Secondary)
class SecondaryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "school",
        "detail_type",
        "total_fee",
        "grade_start",
        "grade_end",
        "toefl_requirement",
        "state",
        "number_i18n_students",
        "program_fee",
        "number_ap_courses",
        "number_honor_courses",
        "number_clubs",
        "number_sports",
        "entry_requirement",
    )

@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "school",
        "detail_type",
        "toefl_requirement",
        "state",
        "national_univ",
        "tuition",
        "room_and_board",
        "sat_act_requirement",
        "sat_25",
        "sat_75",
        "gpa_requirement",
        "ranking",
        "setting",
        "asian_percent",
        "high_school_10",
        "full_time_faculty",
        "student_faculty_ration",
        "class_under_20",
        "ed_ea_deadline",
        "ed_ea_noticedate",
        "application_deadline",
        "degree_offered",
        "most_popular_majors",
        "selling_point",
    )
