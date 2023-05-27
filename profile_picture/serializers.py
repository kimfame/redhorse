from django.conf import settings
from rest_framework import serializers

from profile_picture.models import ProfilePicture


class ProfilePictureSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    main = serializers.BooleanField()
    image = serializers.ImageField()

    def create(self, validated_data):
        user = self.context.get("user")
        profile_picture_count = ProfilePicture.objects.filter(user=user).count()

        if profile_picture_count >= settings.MAX_PROFILE_PICTURE_NUM:
            raise serializers.ValidationError(
                {
                    "image": [
                        f"프로필은 최대 {settings.MAX_PROFILE_PICTURE_NUM}를 초과하여 등록할 수 없습니다."
                    ]
                }
            )

        new_profile_picture = ProfilePicture(
            user=user,
            image=validated_data.get("image"),
        )

        if profile_picture_count == 0:
            new_profile_picture.main = True

        new_profile_picture.save()
        return new_profile_picture

    def update(self, instance, validated_data):
        user_id = self.context.get("user_id")

        if instance.main == True:
            return instance

        if validated_data.get("main") == False:
            return instance

        ProfilePicture.objects.filter(
            user=user_id,
            main=True,
        ).update(main=False)

        instance.main = True
        instance.save()

        return instance
