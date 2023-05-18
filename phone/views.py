from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.utils import get_current_and_past_time
from phone.models import PhoneVerificationHistory
from phone.serializers import (
    PhoneVerificationHistoryCreateSerializer,
    PhoneVerificationHistoryUpdateSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_verification_code(request):
    if request.method == "POST":
        serializer = PhoneVerificationHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_verification_code(request):
    if request.method == "POST":
        serializer = PhoneVerificationHistoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_verified_phone_number(uuid: str) -> PhoneVerificationHistory:
    start_datetime, end_datetime = get_current_and_past_time(
        settings.VERIFIED_PHONE_NUMBER_EXP_TIME
    )

    return PhoneVerificationHistory.objects.filter(
        is_verified=True,
        uuid=uuid,
        created_at__range=(start_datetime, end_datetime),
    ).first()
