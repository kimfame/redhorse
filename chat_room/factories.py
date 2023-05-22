import factory

from factory.django import DjangoModelFactory

from chat_room.models import ChatRoom, ChatRoomMember
from user.factories import UserFactory


class ChatRoomFactory(DjangoModelFactory):
    class Meta:
        model = ChatRoom

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.users.add(user)

        if create:
            return


class ChatRoomMemberFactory(DjangoModelFactory):
    class Meta:
        model = ChatRoomMember

    room = factory.SubFactory(ChatRoomFactory)
    user = factory.SubFactory(UserFactory)
