from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import get_current_and_past_time
from phone.models import PhoneVerificationHistory
from phone.serializers import (
    PhoneVerificationHistoryCreateSerializer,
    PhoneVerificationHistoryUpdateSerializer,
)


class VerificationCodeSender(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneVerificationHistoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeVerification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PhoneVerificationHistoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_verified_phone_number(uuid: str) -> PhoneVerificationHistory:
    start_datetime, end_datetime = get_current_and_past_time(
        settings.VERIFIED_PHONE_NUMBER_EXP_TIME
    )

    return PhoneVerificationHistory.objects.filter(
        is_verified=True,
        uuid=uuid,
        created_at__range=(start_datetime, end_datetime),
    ).first()
