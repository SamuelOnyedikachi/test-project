from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.actions import delete_selected
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    compressed_fields = True
    warn_unsaved_form = True
    fieldsets = UserAdmin.fieldsets + (
        (
            "Safety Profile",
            {
                "fields": (
                    "phone",
                    "full_name",
                    "avatar",
                    "is_verified",
                    "is_emergency_active",
                    "fcm_token",
                    "device_id",
                    "last_latitude",
                    "last_longitude",
                )
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "phone",
        "full_name",
        "is_verified",
        "is_emergency_active",
        "is_active",
        "is_staff",
    )
    list_editable = ("is_verified", "is_emergency_active", "is_active")
    list_filter = UserAdmin.list_filter + ("is_verified", "is_emergency_active")
    search_fields = ("username", "email", "phone", "full_name")
    date_hierarchy = "date_joined"
    save_on_top = True
    actions = (
        "suspend_users",
        "activate_users",
        "verify_users",
        "unverify_users",
        "clear_emergency_status",
        "delete_selected_users",
    )

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.pk == request.user.pk:
            return False
        return super().has_delete_permission(request, obj)

    def delete_model(self, request, obj):
        if obj.pk == request.user.pk:
            messages.error(request, "You cannot delete the account you are currently using.")
            raise PermissionDenied("You cannot delete your own account.")
        super().delete_model(request, obj)

    @admin.action(description="Suspend selected users")
    def suspend_users(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Reactivate selected users")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Verify selected users")
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Mark selected users as unverified")
    def unverify_users(self, request, queryset):
        queryset.update(is_verified=False)

    @admin.action(description="Clear emergency status")
    def clear_emergency_status(self, request, queryset):
        queryset.update(is_emergency_active=False)

    @admin.action(description="Delete selected users")
    def delete_selected_users(self, request, queryset):
        if queryset.filter(pk=request.user.pk).exists():
            messages.warning(
                request,
                "Your current account was removed from the delete selection.",
            )
            queryset = queryset.exclude(pk=request.user.pk)

        if not queryset.exists():
            messages.error(request, "No deletable users were selected.")
            return None

        return delete_selected(self, request, queryset)
