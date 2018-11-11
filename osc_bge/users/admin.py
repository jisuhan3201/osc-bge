from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from osc_bge.users.forms import UserChangeForm, UserCreationForm
from . import models

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("username", "image")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser", "group", "image"]
    search_fields = ["username"]

@admin.register(models.BgeAdminUser)
class BgeAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "partition",
    )

@admin.register(models.BgeBranchAdminUser)
class BgeBranchAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "bge",
        "branch",
    )

@admin.register(models.BgeBranchCoordinator)
class BgeBranchCoordinatorAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "branch_admin",
        "branch",
        "position",
    )

@admin.register(models.AgencyAdminUser)
class AgencyAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "agency",
    )

@admin.register(models.AgencyBranchAdminUser)
class AgencyBranchAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "agency_branch",
    )

@admin.register(models.Counseler)
class CounselerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "coordinator",
        "agency",
        "agency_branch",
    )

@admin.register(models.Host)
class HostAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "coordinator",
        "active_status",
        "phone",
        "status",
        "school",
        "job",
        "employer",
        "is_married",
        "children",
        "pet",
        "plan",
        "gender_hope",
        "student_available",
        "start_date",
        "filename",
        "is_deleted",
    )
