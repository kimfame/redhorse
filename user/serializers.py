import re

from django.core import exceptions
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import serializers

from phone.models import UserPhone
from phone.views import get_verified_phone_number


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
