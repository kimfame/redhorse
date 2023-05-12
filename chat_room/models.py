import uuid

from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    users = models.ManyToManyField(
        User,
        through="ChatRoomMember",
        through_fields=("room", "user"),
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class ChatRoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["room", "user"], name="unique_room_user_combination"
            )
        ]

    def __str__(self):
        return f"{self.room}:{self.user}"
