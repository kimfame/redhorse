import pusher

from dataclasses import dataclass
from uuid import UUID

from django.conf import settings


@dataclass
class PusherMessage:
    room_uuid: str
    user_uuid: str
    message_uuid: str
    message: str
    created_datetime: str

    @property
    def channel(self) -> str:
        return self.room_uuid

    @property
    def event(self) -> str:
        return "new_message"

    @property
    def data(self) -> dict:
        return {
            "user_uuid": self.user_uuid,
            "message_uuid": self.message_uuid,
            "message": self.message,
            "created_datetime": self.created_datetime,
        }


class PusherClient:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=settings.PUSHER_SSL,
        )
        cls.instance = cls.__getInstance
        return cls.__instance


class PusherTransmitter:
    pusher_client = PusherClient.instance()

    @classmethod
    def send_chat_message(cls, message: PusherMessage) -> None:
        cls.pusher_client.trigger(
            message.channel,
            message.event,
            message.data,
        )

    @classmethod
    def leave_chat_room(cls, room_uuid: UUID) -> None:
        cls.pusher_client.trigger(
            str(room_uuid),
            "leave_chat_room",
            {
                "exit": True,
            },
        )
