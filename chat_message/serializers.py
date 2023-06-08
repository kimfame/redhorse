from rest_framework import serializers

from core.pusher import PusherTransmitter, PusherMessage
from chat_message.models import ChatMessage


class ChatMessageListSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = serializers.UUIDField(read_only=True)
    message = serializers.CharField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)


class ChatMessageCreateSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        chat_room_member = self.context.get("chat_room_member")

        new_message = ChatMessage.objects.create(
            room_id=chat_room_member.room.id,
            user=chat_room_member.user,
            message=validated_data.get("message"),
        )

        PusherTransmitter.send_chat_message(
            PusherMessage(
                room_uuid=str(chat_room_member.room.uuid),
                user_uuid=str(chat_room_member.user.profile.uuid),
                message_uuid=str(new_message.uuid),
                message=validated_data.get("message"),
                created_datetime=new_message.created_datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )
        )
        return new_message
