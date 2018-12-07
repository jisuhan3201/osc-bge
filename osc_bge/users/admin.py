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
    fieldsets = (("User", {"fields": ("username", "image", "type")}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "is_superuser", "type", "image"]
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
        "branch",
    )

@admin.register(models.BgeBranchCoordinator)
class BgeBranchCoordinatorAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "branch",
        "position",
    )

@admin.register(models.AgencyHeadAdminUser)
class AgencyHeadAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "agency_head",
    )


@admin.register(models.AgencyAdminUser)
class AgencyAdminUserAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "agency",
    )

@admin.register(models.Counselor)
class CounselorAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "agency",
    )
