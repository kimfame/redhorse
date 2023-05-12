from typing import List

from django.contrib.auth.models import User
from django.db.models import Prefetch, Q, Subquery
from rest_framework import viewsets, status
from rest_framework.response import Response

from chat_room.models import ChatRoom, ChatRoomMember
from chat_room.serializers import ChatRoomListSerializer
from profile_picture.models import ProfilePicture


def create_chat_room(user_list: List[User]):
    chat_room = ChatRoom.objects.create()

    chat_member_list = []

    for user in user_list:
        chat_member = ChatRoomMember(
            room=chat_room,
            user=user,
        )
        chat_member_list.append(chat_member)

    ChatRoomMember.objects.bulk_create(chat_member_list)


class ChatRoomViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user

        prefetch_queryset = ProfilePicture.objects.filter(main=True)
        chat_rooms = (
            ChatRoomMember.objects.select_related("room", "user__profile")
            .prefetch_related(
                Prefetch(
                    "user__profile__profilepicture_set",
                    queryset=prefetch_queryset,
                    to_attr="main_profile_picture",
                )
            )
            .filter(
                ~Q(user=user),
                room__in=Subquery(
                    ChatRoomMember.objects.select_related("room")
                    .filter(user=user, is_active=True)
                    .values("room")
                ),
            )
        )

        serializer = ChatRoomListSerializer(
            chat_rooms,
            many=True,
            context={"user": user},
        )
        return Response(serializer.data)

    def retrieve(self, request, uuid=None):
        pass

    def partial_update(self, request, uuid=None):
        pass
