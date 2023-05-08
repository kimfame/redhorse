from django.conf import settings
from rest_framework import serializers

from profile_picture.models import ProfilePicture


class ProfilePictureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    main = serializers.BooleanField()
    image = serializers.ImageField()

    def create(self, validated_data):
        profile = self.context.get("profile")
        profile_count = ProfilePicture.objects.filter(profile=profile).count()

        if profile_count >= settings.MAX_PROFILE_PICTURE_NUM:
            raise serializers.ValidationError(
                {
                    "image": [
                        f"프로필은 최대 {settings.MAX_PROFILE_PICTURE_NUM}를 초과하여 등록할 수 없습니다."
                    ]
                }
            )

        new_profile_picture = ProfilePicture(
            profile=profile,
            image=validated_data.get("image"),
        )

        if profile_count == 0:
            new_profile_picture.main = True

        new_profile_picture.save()
        return new_profile_picture

    def update(self, instance, validated_data):
        profile = self.context.get("profile")

        if instance.main == True:
            return instance

        ProfilePicture.objects.filter(
            profile=profile,
            main=True,
        ).update(main=False)

        instance.main = True
        instance.save()

        return instance
