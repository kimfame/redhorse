from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response

from chat_message.models import ChatMessage
from chat_message.serializers import (
    ChatMessageCreateSerializer,
    ChatMessageListSerializer,
)
from chat_room.models import ChatRoomMember


class ChatMessageViewSet(viewsets.ViewSet):
    def list(self, request, uuid=None):
        chat_messages = get_list_or_404(
            ChatMessage.objects.select_related("user").order_by("id"),
            room__uuid=uuid,
            room__users__id__exact=request.user.id,
        )
        serializer = ChatMessageListSerializer(chat_messages, many=True)
        return Response(serializer.data)

    def create(self, request, uuid=None):
        user = request.user

        chat_room_member = get_object_or_404(
            ChatRoomMember.objects.select_related("room"),
            room__uuid=uuid,
            room__is_active=True,
            user=user,
            is_active=True,
        )

        serializer = ChatMessageCreateSerializer(
            data=request.data,
            context={
                "user": request.user,
                "room_id": chat_room_member.room_id,
            },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
