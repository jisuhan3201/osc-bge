from django.contrib import admin
from . import models

# Register your models here.
# @admin.register(models.Memo)
# class MemoAdmin(admin.ModelAdmin):
#
#     list_display = (
#         "bge",
#         "branch_admin",
#         "coordinator",
#         "agency_admin",
#         "agency_branch_admin",
#         "counseler",
#         "school",
#         "host",
#         "student",
#         "title",
#         "types",
#         "content",
#         "priority",
#         "filename",
#     )

@admin.register(models.Counsel)
class CounselAdmin(admin.ModelAdmin):

    list_display = (
        "counseler",
        "student",
        "counseling_date",
        "desire_country",
        "program_interested",
        "contact_first",
        "contact_second",
        "contact_third",
        "possibility",
        "expected_departure",
        "client_class",
        "detail",
    )

# @admin.register(models.HomeStay)
# class HomeStayAdmin(admin.ModelAdmin):
#
#     list_display = (
#         "student",
#         "memo",
#         "deadline",
#         "culture_adapt",
#         "culture_improve",
#         "rule_observe",
#         "rule_improve",
#         "arrange_per",
#         "arrange_improve",
#         "conversation_per",
#         "conversation_improve",
#         "timestrict_per",
#         "timestrict_improve",
#         "class_attendancy",
#         "class_attendancy_improve",
#         "filename",
#     )
#
# @admin.register(models.MonthlyReport)
# class MonthlyReportAdmin(admin.ModelAdmin):
#
#     list_display = (
#         "student_coordi",
#         "school_coordi",
#         "host_coordi",
#         "agency_branch_admin",
#         "counseler",
#         "host",
#         "form_homestay",
#         "student",
#         "memo",
#         "title",
#         "category",
#         "priority",
#         "status",
#         "to_parent",
#         "to_agency",
#         "admin_approve",
#         "student_coordi_at",
#         "school_coordi_at",
#         "host_coordi_at",
#         "deadline",
#         "filetype",
#     )


@admin.register(models.Formality)
class FormalityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "counsel",
        "payment_complete",
        "apply_at",
        "canceled_at",
        "cancel_reason",
        "visa_reserve_date",
        "visa_reserve_time",
        "visa_granted_date",
        "visa_granted_time",
        "visa_copy_recieved",
        "visa_rejected_date",
        "visa_rejected_time",
        "eticket_attached",
        "air_departure_date",
        "air_departure_time",
        "air_departure_port",
        "air_arrive_date",
        "air_arrive_time",
        "air_arrive_port",
        "pickup_num",
    )

@admin.register(models.SchoolFormality)
class SchoolFormalityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "school",
        "formality",
        "school_priority",
        "class_start_at",
        "course",
        "processing_fee",
        "processing_fee_done",
    )

@admin.register(models.FormalityFile)
class FormalityFileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "formality",
        "name",
        "file_source",
    )
