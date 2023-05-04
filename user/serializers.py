import logging
import re

from django.conf import settings
from django.core import exceptions
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import serializers

from core.sms import send_sms_message
from core.utils import (
    is_valid_phone_number,
    is_valid_username,
    get_current_and_past_time,
    get_random_string,
)
from user.models import TemporaryPasswordIssueHistory
from phone.models import UserPhone
from phone.views import get_verified_phone_number

logger = logging.getLogger(__name__)


def send_temporary_password(phone_number: str, temporary_password: str):
    message = f"Red Horse에서 보낸 임시 비밀번호 발송문자입니다. 임시 비밀번호는 {temporary_password} 입니다."
    send_sms_message(phone_number=phone_number, message=message)


def validate_password(value: str) -> str:
    try:
        password_validation.validate_password(value)
        return value
    except exceptions.ValidationError as e:
        raise serializers.ValidationError(list(e.messages))


class UserCreateSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = User
        fields = ["username", "password", "uuid"]
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
            "uuid": {"read_only": True},
        }

    def create(self, validated_data):
        phone_verification_history = get_verified_phone_number(
            validated_data.get("uuid")
        )

        if phone_verification_history is None:
            raise serializers.ValidationError(
                {"error": ["휴대폰번호 인증이 만료되었습니다. 휴대폰번호 인증을 다시 시도해주세요."]}
            )

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=validated_data.get("username"),
                    password=validated_data.get("password"),
                )

                UserPhone.objects.create(
                    user=user,
                    phone_number=phone_verification_history.phone_number,
                )

                return user
        except IntegrityError:
            raise serializers.ValidationError(
                {"error": ["계정을 생성할 수 없습니다. 추후 다시 시도해주세요."]}
            )

    def validate_username(self, value):
        regex = re.compile(r"^[\w-]{5,20}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError(
                "5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다."
            )

    def validate_password(self, value):
        return validate_password(value)


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["old_password", "password"]
        extra_kwargs = {
            "old_password": {"write_only": True},
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance

    def validate_old_password(self, value):
        validate_password(value)

        user = self.context.get("user")
        if user.check_password(value):
            return value
        else:
            raise serializers.ValidationError("입력하신 비밀번호가 일치하지 않습니다.")

    def validate_password(self, value):
        return validate_password(value)


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        user_phone = (
            UserPhone.objects.select_related("user")
            .filter(
                phone_number=validated_data.get("phone_number"),
                user__username=validated_data.get("username"),
            )
            .first()
        )

        if user_phone is None:
            logger.info("임시 패스워드 발급 실패")
            logger.info(f"username : {validated_data.get('username')}")
            logger.info(f"phone_number : {validated_data.get('phone_number')}")
            return TemporaryPasswordIssueHistory()

        user = user_phone.user

        start_datetime, end_datetime = get_current_and_past_time(
            settings.PASSWORD_RESET_RETRY_WAIT_TIME
        )

        if TemporaryPasswordIssueHistory.objects.filter(
            user=user,
            created_at__range=(start_datetime, end_datetime),
        ).exists():
            raise serializers.ValidationError(
                {
                    "error": [
                        f"임시 비밀번호 발급을 시도한 이력이 있습니다. {settings.PASSWORD_RESET_RETRY_WAIT_TIME}분 후 다시 시도해주세요."
                    ]
                }
            )

        new_temporary_password_issue_history = (
            TemporaryPasswordIssueHistory.objects.create(
                user=user,
            )
        )

        send_temporary_password(
            phone_number=user_phone.phone_number,
            temporary_password=self._change_to_temporary_password(user),
        )

        return new_temporary_password_issue_history

    def validate_phone_number(self, value):
        if is_valid_phone_number(value):
            return value
        else:
            raise serializers.ValidationError(
                "입력된 휴대폰번호의 형식이 잘못되었습니다. 띄어쓰기 없이 하이픈(-)을 제외하고 입력해주세요."
            )

    def validate_username(self, value):
        if is_valid_username(value):
            return value
        else:
            raise serializers.ValidationError(
                "5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다."
            )

    def _change_to_temporary_password(self, user: User) -> str:
        temporary_password = get_random_string(10)
        user.set_password(temporary_password)
        user.save()
        return temporary_password
