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
        "partnership",
        "provider",
        "provider_branch",
        "admission_coordi",
        "school_coordi",
        "term",
        "transfer",
        "country",
        "address",
        "area_description",
        "phone",
        "web_url",
        "founded",
        "religion",
        "number_students",
    )

@admin.register(models.Secondary)
class SecondaryAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "grade_start",
        "grade_end",
        "accept_12_grade",
        "application_fee",
        "program_fee",
        "admission_requirements",
        "admission_documents",
        "selling_point",
        "state",
        "student_body",
        "international_students",
        "esl",
        "student_teach_ratio",
        "class_size",
        "uniform",
        "college_acceptance_rate",
        "avg_sat",
        "number_honor_courses",
        "list_honor_courses",
        "number_ap_courses",
        "list_ap_courses",
        "number_clubs",
        "number_sports",
        "facilities",
    )

@admin.register(models.College)
class CollegeAdmin(admin.ModelAdmin):

    list_display = (
        "school",
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

@admin.register(models.SchoolTypes)
class SchoolTypesAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "type",
    )

@admin.register(models.SchoolPhotos)
class SchoolPhotosAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "photo",
    )
