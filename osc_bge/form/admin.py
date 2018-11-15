from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Memo)
class MemoAdmin(admin.ModelAdmin):

    list_display = (
        "bge",
        "branch_admin",
        "coordinator",
        "agency_admin",
        "agency_branch_admin",
        "counseler",
        "school",
        "host",
        "student",
        "title",
        "types",
        "content",
        "priority",
        "filename",
    )

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

@admin.register(models.HomeStay)
class HomeStayAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "memo",
        "deadline",
        "culture_adapt",
        "culture_improve",
        "rule_observe",
        "rule_improve",
        "arrange_per",
        "arrange_improve",
        "conversation_per",
        "conversation_improve",
        "timestrict_per",
        "timestrict_improve",
        "class_attendancy",
        "class_attendancy_improve",
        "filename",
    )

@admin.register(models.MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):

    list_display = (
        "student_coordi",
        "school_coordi",
        "host_coordi",
        "agency_branch_admin",
        "counseler",
        "host",
        "form_homestay",
        "student",
        "memo",
        "title",
        "category",
        "priority",
        "status",
        "to_parent",
        "to_agency",
        "admin_approve",
        "student_coordi_at",
        "school_coordi_at",
        "host_coordi_at",
        "deadline",
        "filetype",
    )


@admin.register(models.Formality)
class FormalityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "counsel",
        "payment_complete",
        "apply_at",
        "canceled_at",
        "visa_reserve_at",
        "visa_approve_at",
        "visa_denied_at",
        "departure_ot_at",
        "departure_complete",
        "air_ticketing_at",
        "air_departure_at",
        "air_arrive_at",
        "air_departure_port",
        "air_arrive_port",
        "pickup_num",
        "pickup_at",
        "is_pet",
        "is_child",
        "is_allergy",
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
        "form_apply_fee",
        "entrance_grade",
        "entrance_fee",
        "entrance_prefee",
        "entrance_restfee",
        "interview_reserve_at",
        "training_reserve_at",
        "entrance_approve_at",
        "entrance_canceled_at",
        "i20_apply_at",
        "i20_fee",
        "i20_prefee",
        "i20_restfee",
        "i20_receive_at",
        "program_fee_complete",
        "program_fee_send_at",
        "program_fee",
        "program_prefee",
        "program_restfee",
    )
