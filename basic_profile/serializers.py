import re

from django.conf import settings
from rest_framework import serializers

from core.utils import is_adult
from basic_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "uuid",
            "nickname",
            "birthdate",
            "gender",
            "preferred_gender",
            "mbti",
            "passion",
            "height",
            "religion",
            "smoking_status",
            "drinking_status",
            "location",
            "bio",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context.get("user")

        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError({"error": ["프로필이 이미 존재합니다."]})

        validated_data["user"] = user

        return super(ProfileSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        update_target_fields = [
            "nickname",
            "preferred_gender",
            "mbti",
            "passion",
            "height",
            "religion",
            "smoking_status",
            "drinking_status",
            "location",
            "bio",
        ]

        new_validated_data = {
            field: value
            for field, value in validated_data.items()
            if field in update_target_fields
        }

        return super(ProfileSerializer, self).update(instance, new_validated_data)

    def validate_birthdate(self, value):
        if is_adult(value) is False:
            raise serializers.ValidationError("미성년자는 해당 서비스를 이용하실 수 없습니다.")
        else:
            return value

    def validate_gender(self, value):
        regex = re.compile(r"^[MF]{1}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError("잘못된 성별 정보를 입력하셨습니다.")

    def validate_preferred_gender(self, value):
        regex = re.compile(r"^[MFA]{1}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError("잘못된 선호 성별 정보를 입력하셨습니다.")

    def validate_mbti(self, value):
        regex = re.compile(r"^[EI]{1}[NS]{1}[FT]{1}[JP]{1}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError("잘못된 MBTI 정보를 입력하셨습니다.")

    def validate_height(self, value):
        regex = re.compile(r"^[12]{1}[0-9]{2}$")

        if regex.search(value):
            return value
        else:
            raise serializers.ValidationError("잘못된 신장 정보를 입력하셨습니다.")

    def validate_passion(self, value):
        if len(value) > settings.MAX_PASSION_NUM:
            raise serializers.ValidationError(
                f"취미는 최대 {settings.MAX_PASSION_NUM}개를 초과할 수 없습니다."
            )

        return value

    def validate_drinking_status(self, value):
        regex = re.compile(r"^[ㄱ-ㅣ가-힣]{2}$")

        if regex.search(value) is None:
            raise serializers.ValidationError("잘못된 음주 빈도 정보를 입력하셨습니다.")

        common_code_queryset = self.context.get("common_code_queryset")

        drinking_status_types = [
            common_code.value
            for common_code in common_code_queryset
            if common_code.group.name == "drinking_status"
        ]

        if value in drinking_status_types:
            return value
        else:
            raise serializers.ValidationError("잘못된 음주 빈도 정보를 입력하셨습니다.")

    def validate_religion(self, value):
        common_code_queryset = self.context.get("common_code_queryset")

        religion_types = [
            common_code.value
            for common_code in common_code_queryset
            if common_code.group.name == "religion"
        ]

        if value in religion_types:
            return value
        else:
            raise serializers.ValidationError("잘못된 종교 정보를 입력하셨습니다.")

    def validate_location(self, value):
        regex = re.compile(r"^[ㄱ-ㅣ가-힣]{2}$")

        if regex.search(value) is None:
            raise serializers.ValidationError("잘못된 지역 정보를 입력하셨습니다.")

        common_code_queryset = self.context.get("common_code_queryset")

        location_types = [
            common_code.value
            for common_code in common_code_queryset
            if common_code.group.name == "location"
        ]

        if value in location_types:
            return value
        else:
            raise serializers.ValidationError("잘못된 위치 정보를 입력하셨습니다.")
