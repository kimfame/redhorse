from rest_framework import serializers


class ChatRoomListSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    nickname = serializers.CharField()
    image = serializers.CharField()

    # room = serializers.SerializerMethodField()
    # nickname = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()

    # def get_room(self, obj):
    #     return obj.room.uuid

    # def get_nickname(self, obj):
    #     return obj.user.profile.nickname

    # def get_image(self, obj):
    #     profile_picture_list = obj.user.profile.main_profile_picture
    #     main_profile_picture = (
    #         profile_picture_list[0].image.url if profile_picture_list else None
    #     )
    #     return main_profile_picture


class ChatRoomRetrieveSerializer(serializers.Serializer):
    uuid = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_uuid(self, obj):
        return obj.user.profile.uuid

    def get_nickname(self, obj):
        return obj.user.profile.nickname

    def get_image(self, obj):
        profile_picture_list = obj.user.profile.main_profile_picture
        main_profile_picture = (
            profile_picture_list[0].image.url if profile_picture_list else None
        )
        return main_profile_picture
