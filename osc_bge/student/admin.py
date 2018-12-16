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
        "counselor",
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

@admin.register(models.CurrentStudentReview)
class CurrentStudentReviewAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "student",
        "grade",
        "homecity",
        "comment",
    )

@admin.register(models.GraduateStudentReview)
class GraduateStudentReviewAdmin(admin.ModelAdmin):

    list_display = (
        "school",
        "student",
        "attended",
        "init_eng",
        "gpa_china",
        "toefl",
        "gpa",
        "sat_act",
        "activities",
        "college",
        "major",
    )


@admin.register(models.StudentMonthlyReport)
class StudentMonthlyReportAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "counseling_date",
        "manager_confirm_date",
        "school_year",
        "grade",
        "send_to_agent_date",
        "college_plan",
        "eng9h_lv",
        "eng9h_tg",
        "eng9h_current",
        "precal_lv",
        "precal_tg",
        "precal_current",
        "bioh_lv",
        "bioh_tg",
        "bioh_current",
        "chemh_lv",
        "chemh_tg",
        "chemh_current",
        "geo_lv",
        "geo_tg",
        "geo_current",
        "cs_lv",
        "cs_tg",
        "cs_current",
        "sp_lv",
        "sp_tg",
        "sp_current",
        "orch_lv",
        "orch_tg",
        "orch_current",
        "comment",
        "target_gpa",
        "transcript",
        "eng_skill",
        "toefl",
        "toefl_reading",
        "toefl_listening",
        "toefl_speaking",
        "toefl_writing",
        "toefl_total",
        "toefl_target",
        "toefl_next_test_date",
        "sat",
        "sat_evb_reading_writing",
        "sat_math",
        "sat_total",
        "sat_target",
        "sat_next_test_date",
        "act",
        "act_eng",
        "act_math",
        "act_reading",
        "act_sci",
        "act_composition_score",
        "act_target",
        "act_next_test_date",
        "ap_tests",
        "sat_subjects_tests",
        "test_prep",
        "activities",
        "community_services",
        "agenda",
        "comment2",
        "objective_assignment",
        "payment_desc",
        "payment_expense",
        "payment_due_date",
        "payment_payment",
        "payment_paid_date",
        "payment_balance",
        "payment_invoice",
        "submit_date",
        "agent_confirmed",
        "status",
        "created_at",
        "updated_at",
    )

@admin.register(models.StudentAccounting)
class StudentAccountingAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "description",
        "expense",
        "due_date",
        "payment",
        "paid_date",
        "balance",
        "invoice",
    )
