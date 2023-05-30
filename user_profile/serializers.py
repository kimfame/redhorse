from rest_framework import serializers

from core.utils import calculate_age, get_option_code_list, is_adult
from user_profile.models import Profile


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

    def validate_birthdate(self, value):
        if is_adult(value) is False:
            raise serializers.ValidationError("미성년자는 해당 서비스를 이용하실 수 없습니다.")
        else:
            return value

    def validate_passions(self, value):
        if value:
            passions = get_option_code_list("passion")

            for new_passion in value:
                if new_passion in passions:
                    pass
                else:
                    raise serializers.ValidationError("잘못된 취미를 선택하셨습니다. 다시 시도하세요.")

        return value


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
    passions = serializers.JSONField(read_only=True)
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
