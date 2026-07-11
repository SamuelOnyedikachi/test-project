import secrets

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.template.response import TemplateResponse
from django.urls import reverse
from unfold.admin import ModelAdmin

from .models import DeveloperApiKey, LocationViewAudit, RoutePoint, TrackingSession


@admin.register(TrackingSession)
class TrackingSessionAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = (
        "id",
        "user",
        "status",
        "emergency",
        "started_at",
        "ended_at",
        "updated_at",
    )
    list_filter = ("status", "emergency", "started_at")
    list_editable = ("status",)
    search_fields = ("user__username", "user__email", "user__phone")
    readonly_fields = ("started_at", "ended_at", "updated_at")
    filter_horizontal = ("assigned_organizations",)
    fieldsets = (
        (
            "Session",
            {
                "fields": (
                    "user",
                    "assigned_organizations",
                    "status",
                    "emergency",
                    "public_share_token",
                    "expires_at",
                )
            },
        ),
        (
            "Latest Location",
            {
                "fields": (
                    "latest_latitude",
                    "latest_longitude",
                    "latest_accuracy",
                    "latest_speed",
                    "latest_heading",
                    "latest_altitude",
                )
            },
        ),
        ("Timeline", {"fields": ("started_at", "ended_at", "updated_at")}),
    )


@admin.register(RoutePoint)
class RoutePointAdmin(ModelAdmin):
    compressed_fields = True
    list_display = (
        "id",
        "session",
        "latitude",
        "longitude",
        "speed",
        "recorded_at",
    )
    list_filter = ("recorded_at",)
    search_fields = ("session__user__username", "session__user__phone")
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Session",
            {"fields": ("session", "recorded_at", "created_at")},
        ),
        (
            "Location",
            {
                "fields": (
                    "latitude",
                    "longitude",
                    "accuracy",
                    "altitude",
                    "heading",
                    "speed",
                )
            },
        ),
        (
            "Device Context",
            {"fields": ("battery_level", "network_type")},
        ),
    )


@admin.register(LocationViewAudit)
class LocationViewAuditAdmin(ModelAdmin):
    compressed_fields = True
    list_display = ("id", "session", "viewer", "api_key_name", "ip_address", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("viewer__username", "api_key_name", "ip_address")
    readonly_fields = ("viewed_at",)


@admin.register(DeveloperApiKey)
class DeveloperApiKeyAdmin(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_display = (
        "id",
        "owner",
        "name",
        "key_prefix",
        "is_active",
        "rate_limit_per_minute",
        "created_at",
        "last_used_at",
    )
    list_filter = ("is_active", "created_at")
    list_editable = ("is_active", "rate_limit_per_minute")
    search_fields = ("owner__username", "name", "key_prefix")
    readonly_fields = ("key_prefix", "created_at", "last_used_at")
    fieldsets = (
        (
            "Developer App",
            {"fields": ("owner", "name", "is_active", "notes")},
        ),
        (
            "Access Control",
            {
                "fields": (
                    "scopes",
                    "allowed_origins",
                    "allowed_ips",
                    "webhook_url",
                    "rate_limit_per_minute",
                ),
                "description": (
                    "Use scopes such as tracking:read, tracking:write, "
                    "emergency:read, geofences:read, webhooks:write."
                ),
            },
        ),
        (
            "Key Metadata",
            {"fields": ("key_prefix", "created_at", "last_used_at")},
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change or not obj.hashed_key:
            raw_key = f"nvg_{secrets.token_urlsafe(32)}"
            obj.key_prefix = raw_key[:12]
            obj.hashed_key = make_password(raw_key)
            request._navigo_raw_api_key = raw_key
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        raw_key = getattr(request, "_navigo_raw_api_key", None)
        if raw_key:
            return TemplateResponse(
                request,
                "admin/tracking/developerapikey/key_created.html",
                {
                    **self.admin_site.each_context(request),
                    "title": "Developer API key created",
                    "opts": self.model._meta,
                    "object": obj,
                    "raw_key": raw_key,
                    "change_url": reverse(
                        "admin:tracking_developerapikey_change",
                        args=[obj.pk],
                    ),
                    "list_url": reverse("admin:tracking_developerapikey_changelist"),
                },
            )
        return super().response_add(request, obj, post_url_continue)
