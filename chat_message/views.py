from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from chat_message.models import ChatMessage
from chat_message.paginations import ChatMessagePagination
from chat_message.serializers import (
    ChatMessageCreateSerializer,
    ChatMessageListSerializer,
)
from chat_room.models import ChatRoomMember


class ChatMessageListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ChatMessageListSerializer
    pagination_class = ChatMessagePagination

    def list(self, request, uuid=None, *args, **kwargs):
        queryset = get_list_or_404(
            ChatMessage.objects.select_related("user").order_by("id"),
            room__uuid=uuid,
            room__users__id__exact=request.user.id,
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CreateChatMessage(APIView):
    def post(self, request, uuid=None):
        user_id = request.user.id

        chat_room_member = get_object_or_404(
            ChatRoomMember.objects.select_related("room"),
            room__uuid=uuid,
            room__is_active=True,
            user=user_id,
            is_active=True,
        )

        serializer = ChatMessageCreateSerializer(
            data=request.data,
            context={
                "user_id": user_id,
                "room_id": chat_room_member.room_id,
            },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
