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
        "counselor",
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
        "enrolment_apply_fee",
        "enrolment_apply_done",
        "enrolment_apply_done_date",
        "prepared_passport",
        "prepared_transcript",
        "prepared_eng_exams",
        "prepared_recommendation",
        "prepared_essay",
        "school_interview_date",
        "school_interview_time",
        "mock_interview",
        "school_interview_done",
        "acceptance_date",
        "acceptance_letter",
        "cancel_enrolment_date",
        "cancel_enrolment_time",
        "i20_completed",
        "i20_fee",
        "i20_receipt",
        "i20_received_date",
        "i20_copy",
        "i20_tracking",
        "provider_application",
        "bge_program_application",
        "immunization",
        "financial_support",
        "program_fee_completed",
        "program_fee",
        "program_fee_receipt",
    )

@admin.register(models.FormalityFile)
class FormalityFileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "formality",
        "name",
        "file_source",
    )
