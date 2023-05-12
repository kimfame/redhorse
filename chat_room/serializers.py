from rest_framework import serializers


class ChatRoomListSerializer(serializers.Serializer):
    room = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    def get_room(self, obj):
        return obj.room.uuid

    def get_nickname(self, obj):
        return obj.user.profile.nickname

    def get_profile_picture(self, obj):
        main_profile_picture = obj.user.profile.main_profile_picture
        return main_profile_picture[0].image.url if main_profile_picture else None
