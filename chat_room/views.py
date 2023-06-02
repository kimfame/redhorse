import logging

from django.shortcuts import get_object_or_404
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.response import Response

from chat_room.models import ChatRoomMember
from chat_room.serializers import ChatRoomListSerializer, ChatRoomRetrieveSerializer
from core.pusher import PusherTransmitter
from core.queries import chat_room_list_query
from profile_picture.models import ProfilePicture


logger = logging.getLogger(__name__)


class ChatRoomViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.user.id

        chat_room_list = ProfilePicture.objects.raw(
            chat_room_list_query, {"id": str(user_id)}
        )

        serializer = ChatRoomListSerializer(
            chat_room_list,
            many=True,
        )
        return Response(serializer.data)

    def retrieve(self, request, uuid=None):
        user_id = request.user.id

        prefetch_queryset = ProfilePicture.objects.order_by("-main", "id")[:1]
        chat_room_members = (
            ChatRoomMember.objects.select_related("room", "user__profile")
            .prefetch_related(
                Prefetch(
                    "user__profilepicture_set",
                    queryset=prefetch_queryset,
                    to_attr="main_profile_picture",
                )
            )
            .filter(
                room__uuid=uuid,
                room__users__id__exact=user_id,
            )
            .exclude(user=user_id)
        )

        serializer = ChatRoomRetrieveSerializer(
            chat_room_members,
            many=True,
        )

        return Response({"room": uuid, "users": serializer.data})

    def partial_update(self, request, uuid=None):
        user_id = request.user.id
        chat_room_member = get_object_or_404(
            ChatRoomMember.objects.select_related("room"),
            room__uuid=uuid,
            user=user_id,
            is_active=True,
        )

        chat_room = chat_room_member.room
        chat_room.is_active = False
        chat_room_member.is_active = False

        try:
            with transaction.atomic():
                chat_room.save()
                chat_room_member.save()
        except IntegrityError as e:
            logger.error(e)
            return Response(
                {"error": ["시스템 에러로 인해서 채팅방을 나갈 수 없습니다. 추후 다시 시도해주세요."]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        PusherTransmitter.leave_chat_room(chat_room.uuid)

        return Response(status=status.HTTP_204_NO_CONTENT)
