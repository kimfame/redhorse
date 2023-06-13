from django.conf import settings
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from core.utils import get_current_and_past_time
from phone.models import PhoneVerificationHistory
from phone.serializers import (
    PhoneVerificationHistoryCreateSerializer,
    PhoneVerificationHistoryUpdateSerializer,
)


class VerificationCodeSender(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationHistoryCreateSerializer
    http_method_names = ["post"]


class CodeVerification(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = PhoneVerificationHistoryUpdateSerializer
    http_method_names = ["post"]


def get_verified_phone_number(uuid: str) -> PhoneVerificationHistory:
    start_datetime, end_datetime = get_current_and_past_time(
        settings.VERIFIED_PHONE_NUMBER_EXP_TIME
    )

    return PhoneVerificationHistory.objects.filter(
        is_verified=True,
        uuid=uuid,
        created_datetime__range=(start_datetime, end_datetime),
    ).first()
