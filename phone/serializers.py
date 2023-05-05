import random
import re

from django.conf import settings
from rest_framework import serializers

from core.utils import is_valid_phone_number, get_current_and_past_time
from core.sms import send_sms_message
from phone.models import PhoneVerificationHistory, UserPhone


def send_verification_code(phone_number, verification_code):
    message = f"Red Horse에서 보낸 인증번호 [{verification_code}]입니다."
    send_sms_message(phone_number=phone_number, message=message)


class PhoneVerificationHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerificationHistory
        fields = ["phone_number"]
        extra_kwargs = {
            "phone_number": {"write_only": True},
        }

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        verification_code = str(random.randint(100000, 999999))

        phone_verification_history = PhoneVerificationHistory.objects.create(
            phone_number=phone_number,
            verification_code=verification_code,
        )

        send_verification_code(
            phone_number=phone_number,
            verification_code=verification_code,
        )

        return phone_verification_history

    def validate_phone_number(self, value):
        if is_valid_phone_number(value) is False:
            raise serializers.ValidationError(
                "입력된 휴대폰번호의 형식이 잘못되었습니다. 띄어쓰기 없이 하이픈(-)을 제외하고 입력해주세요."
            )

        start_datetime, end_datetime = get_current_and_past_time(
            settings.VERIFICATION_CODE_EXP_TIME
        )

        does_exist_phone_verification_history = PhoneVerificationHistory.objects.filter(
            phone_number=value,
            created_at__range=(start_datetime, end_datetime),
        ).exists()

        if does_exist_phone_verification_history is True:
            raise serializers.ValidationError(
                f"이미 인증을 시도하였습니다. {settings.VERIFICATION_CODE_EXP_TIME}분 후 다시 시도해주세요."
            )

        if UserPhone.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("이미 가입되었거나 사용할 수 없는 휴대폰번호입니다.")

        return value


class PhoneVerificationHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneVerificationHistory
        fields = [
            "phone_number",
            "verification_code",
            "uuid",
        ]
        extra_kwargs = {
            "phone_number": {"write_only": True},
            "verification_code": {"write_only": True},
            "uuid": {"read_only": True},
        }

    def create(self, validated_data):
        start_datetime, end_datetime = get_current_and_past_time(
            settings.VERIFICATION_CODE_EXP_TIME
        )

        phone_verification_history = (
            PhoneVerificationHistory.objects.filter(
                phone_number=validated_data.get("phone_number"),
                verification_code=validated_data.get("verification_code"),
                created_at__range=(start_datetime, end_datetime),
            )
            .order_by("-created_at")
            .first()
        )

        if phone_verification_history:
            if phone_verification_history.is_verified is False:
                phone_verification_history.is_verified = True
                phone_verification_history.save()

            return phone_verification_history
        else:
            raise serializers.ValidationError(
                {"verification_code": ["인증번호가 일치하지 않습니다. 다시 입력해주세요."]}
            )

    def validate_phone_number(self, value):
        if is_valid_phone_number(value):
            return value
        else:
            raise serializers.ValidationError(
                "입력된 휴대폰번호의 형식이 잘못되었습니다. 띄어쓰기 없이 하이픈(-)을 제외하고 입력해주세요."
            )

    def validate_verification_code(self, value):
        regex = re.compile(r"^\d{6}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError("입력된 인증코드의 형식이 잘못되었습니다. 숫자 6자리를 입력해주세요.")

    def validate_created_at(self, value):
        start_datetime, end_datetime = get_current_and_past_time(
            settings.VERIFICATION_CODE_EXP_TIME
        )

        if end_datetime > value and value > start_datetime:
            return value
        else:
            raise serializers.ValidationError("인증시간이 지났습니다. 다시 시도해주세요.")
