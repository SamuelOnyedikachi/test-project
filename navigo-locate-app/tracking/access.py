from django.db.models import Q
from organizations.models import OrganizationMember

from .models import TrackingSession


def sessions_visible_to(user):
    queryset = TrackingSession.objects.all()
    if not user or not user.is_authenticated:
        return queryset.none()
    if user.is_staff:
        return queryset
    return queryset.filter(
        Q(user=user)
        | Q(
            assigned_organizations__members__user=user,
            assigned_organizations__members__is_active=True,
            assigned_organizations__members__role__in=(
                OrganizationMember.OPERATIONAL_ROLES
            ),
        )
    ).distinct()
