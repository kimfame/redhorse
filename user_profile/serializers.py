import re

from django.conf import settings
from rest_framework import serializers

from core.utils import calculate_age, is_adult
from user_profile.models import Profile
from passion.serializers import PassionSerializer


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "nickname",
            "birthdate",
            "gender",
            "preferred_gender",
            "mbti",
            "passions",
            "height",
            "religion",
            "smoking_status",
            "drinking_status",
            "location",
            "bio",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["passions"] = PassionSerializer(instance.passions.all(), many=True).data
        return ret

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

    def validate_passions(self, value):
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


class CreateMyProfileSerializer(MyProfileSerializer):
    class Meta(MyProfileSerializer.Meta):
        model = Profile
        fields = MyProfileSerializer.Meta.fields
        extra_kwargs = {
            "nickname": {"required": True},
            "birthdate": {"required": True},
            "gender": {"required": True},
            "preferred_gender": {"required": True},
            "mbti": {"required": True},
            "passions": {"required": True},
            "height": {"required": True},
            "religion": {"required": True},
            "smoking_status": {"required": True},
            "drinking_status": {"required": True},
            "location": {"required": True},
            "bio": {"required": True},
        }

    def create(self, validated_data):
        user = self.context.get("user")

        if Profile.objects.filter(user=user).exists():
            raise serializers.ValidationError({"error": ["프로필이 이미 존재합니다."]})

        validated_data["user"] = user

        return super(CreateMyProfileSerializer, self).create(validated_data)


class UpdateMyProfileSerializer(MyProfileSerializer):
    class Meta:
        model = Profile
        fields = [
            "nickname",
            "preferred_gender",
            "mbti",
            "passions",
            "height",
            "religion",
            "smoking_status",
            "drinking_status",
            "location",
            "bio",
        ]
        extra_kwargs = {
            "nickname": {"required": False},
            "preferred_gender": {"required": False},
            "mbti": {"required": False},
            "passions": {"required": False},
            "height": {"required": False},
            "religion": {"required": False},
            "smoking_status": {"required": False},
            "drinking_status": {"required": False},
            "location": {"required": False},
            "bio": {"required": False},
        }


class OppositeProfileSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    nickname = serializers.CharField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    gender = serializers.CharField(read_only=True)
    mbti = serializers.CharField(read_only=True)
    passions = PassionSerializer(many=True)
    height = serializers.CharField(read_only=True)
    religion = serializers.CharField(read_only=True)
    smoking_status = serializers.BooleanField(read_only=True)
    drinking_status = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)
    bio = serializers.CharField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    def get_age(self, obj):
        return calculate_age(obj.birthdate)

    def get_images(self, obj):
        return [
            profile_picture.image.url for profile_picture in obj.user.profile_pictures
        ]
