import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from .models import PasswordResetOTP

logger = logging.getLogger(__name__)
MAX_OTP_ATTEMPTS = 5
MAX_OTP_REQUESTS_PER_HOUR = 5


def request_password_reset(user, requested_ip=None):
    now = timezone.now()
    recent_count = PasswordResetOTP.objects.filter(
        user=user,
        created_at__gte=now - timedelta(hours=1),
    ).count()
    if recent_count >= MAX_OTP_REQUESTS_PER_HOUR:
        return False

    code = f"{secrets.randbelow(1_000_000):06d}"
    with transaction.atomic():
        PasswordResetOTP.objects.filter(
            user=user,
            consumed_at__isnull=True,
        ).update(consumed_at=now)
        otp = PasswordResetOTP.objects.create(
            user=user,
            code_hash=make_password(code),
            expires_at=now + timedelta(minutes=settings.PASSWORD_RESET_OTP_MINUTES),
            requested_ip=requested_ip,
        )

    try:
        send_mail(
            subject="Your NaviGo-Locate password reset code",
            message=(
                f"Hello {user.get_username()},\n\n"
                f"Your NaviGo-Locate password reset code is: {code}\n\n"
                f"This code expires in {settings.PASSWORD_RESET_OTP_MINUTES} minutes. "
                "Do not share it with anyone. If you did not request this reset, "
                "you can ignore this email.\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        otp.consumed_at = timezone.now()
        otp.save(update_fields=["consumed_at"])
        logger.exception("Unable to send password reset email for user %s", user.pk)
        return False
    return True


def reset_password_with_otp(user, code, new_password):
    now = timezone.now()
    with transaction.atomic():
        otp = (
            PasswordResetOTP.objects.select_for_update()
            .filter(user=user, consumed_at__isnull=True)
            .order_by("-created_at")
            .first()
        )
        if otp is None or otp.expires_at <= now or otp.attempts >= MAX_OTP_ATTEMPTS:
            return False

        if not check_password(code, otp.code_hash):
            otp.attempts += 1
            if otp.attempts >= MAX_OTP_ATTEMPTS:
                otp.consumed_at = now
                otp.save(update_fields=["attempts", "consumed_at"])
            else:
                otp.save(update_fields=["attempts"])
            return False

        user.set_password(new_password)
        user.save(update_fields=["password"])
        PasswordResetOTP.objects.filter(
            user=user,
            consumed_at__isnull=True,
        ).update(consumed_at=now)
        return True
