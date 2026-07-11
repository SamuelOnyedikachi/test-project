from django.contrib import admin

from .models import Organization, OrganizationMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization_type", "phone", "is_verified", "created_at")
    list_filter = ("organization_type", "is_verified", "created_at")
    list_editable = ("organization_type", "is_verified")
    search_fields = ("name", "phone", "email", "address")
    fieldsets = (
        ("Organization", {"fields": ("name", "organization_type", "is_verified")}),
        ("Contact", {"fields": ("phone", "email", "address")}),
    )


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "user", "role", "is_active", "joined_at")
    list_filter = ("role", "is_active", "joined_at")
    list_editable = ("role", "is_active")
    search_fields = ("organization__name", "user__username", "user__email")
    readonly_fields = ("joined_at",)
