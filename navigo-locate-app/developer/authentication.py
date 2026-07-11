from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import authentication, exceptions

from tracking.models import DeveloperApiKey


class ApiKeyAuthentication(authentication.BaseAuthentication):
    keyword = "Api-Key"

    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header.startswith(self.keyword):
            return None

        raw_key = header.removeprefix(self.keyword).strip()
        if not raw_key:
            raise exceptions.AuthenticationFailed("Missing API key.")

        key_prefix = raw_key[:12]
        candidates = DeveloperApiKey.objects.select_related("owner").filter(
            key_prefix=key_prefix,
            is_active=True,
        )
        for api_key in candidates:
            if check_password(raw_key, api_key.hashed_key):
                api_key.last_used_at = timezone.now()
                api_key.save(update_fields=["last_used_at"])
                request.developer_api_key = api_key
                return (api_key.owner, api_key)

        raise exceptions.AuthenticationFailed("Invalid API key.")
