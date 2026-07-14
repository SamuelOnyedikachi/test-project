from django import forms
from django.contrib.auth import get_user_model
from django.db import models

from .models import Notification


class NotificationAdminForm(forms.ModelForm):
    class Audience(models.TextChoices):
        SINGLE = "single", "One user"
        SELECTED = "selected", "Selected users"
        ALL = "all", "All active registered users"

    audience = forms.ChoiceField(
        choices=Audience.choices,
        initial=Audience.SINGLE,
        help_text="Choose whether this form creates one notification or a copy for multiple registered users.",
    )
    selected_users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        help_text="Used only for Selected users. Hold Ctrl/Cmd to select more than one user.",
    )

    class Meta:
        model = Notification
        fields = "__all__"
        help_texts = {
            "user": "Required when Audience is One user.",
            "channel": "Push creates an in-app message. SMS and email require an external delivery provider.",
            "recipient": "Optional provider address such as a phone number or email; leave empty for in-app push.",
            "provider": "Optional delivery provider identifier. Use in_app for app-only messages.",
            "provider_message_id": "Identifier returned by an external provider after delivery.",
            "error_message": "Delivery failure details; normally populated by a worker rather than entered manually.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].required = False
        self.fields["selected_users"].queryset = get_user_model().objects.filter(is_active=True).order_by("username")
        if self.instance.pk:
            self.fields["audience"].disabled = True
            self.fields["selected_users"].disabled = True

    def clean(self):
        cleaned = super().clean()
        if self.instance.pk:
            return cleaned
        audience = cleaned.get("audience")
        if audience == self.Audience.SINGLE and not cleaned.get("user"):
            self.add_error("user", "Select the recipient for this notification.")
        if audience == self.Audience.SELECTED and not cleaned.get("selected_users"):
            self.add_error("selected_users", "Select at least one registered user.")
        if audience == self.Audience.ALL and not get_user_model().objects.filter(is_active=True).exists():
            self.add_error("audience", "There are no active registered users.")
        return cleaned

    def recipients(self):
        if self.instance.pk or self.cleaned_data["audience"] == self.Audience.SINGLE:
            return [self.cleaned_data["user"]]
        if self.cleaned_data["audience"] == self.Audience.ALL:
            return list(get_user_model().objects.filter(is_active=True).order_by("pk"))
        return list(self.cleaned_data["selected_users"].order_by("pk"))
