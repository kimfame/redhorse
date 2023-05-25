import uuid

from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel
from chat_room.models import ChatRoom


class ChatMessage(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"{str(self.id)}:{self.message[:10] if self.message else ''}"
