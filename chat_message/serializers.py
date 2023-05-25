from rest_framework import serializers

from chat_message.models import ChatMessage


class ChatMessageListSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    user = serializers.UUIDField(read_only=True)
    message = serializers.CharField(read_only=True)
    created_datetime = serializers.DateTimeField(read_only=True)


class ChatMessageCreateSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        room_id = self.context.get("room_id")

        return ChatMessage.objects.create(
            room_id=room_id,
            user_id=user_id,
            message=validated_data.get("message"),
        )
