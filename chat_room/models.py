import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel


class ChatRoom(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    users = models.ManyToManyField(
        User,
        through="ChatRoomMember",
        through_fields=("room", "user"),
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class ChatRoomMember(TimeStampedModel):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "user"], name="unique_room_user_combination"
            )
        ]

    def __str__(self):
        return f"{self.room}:{self.user}"
