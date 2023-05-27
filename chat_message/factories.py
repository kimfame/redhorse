import factory
from faker import Faker

from factory.django import DjangoModelFactory

from chat_message.models import ChatMessage
from chat_room.factories import ChatRoomFactory
from user.factories import UserFactory

fake = Faker()


class ChatMessageFactory(DjangoModelFactory):
    class Meta:
        model = ChatMessage

    room = factory.SubFactory(ChatRoomFactory)
    user = factory.SubFactory(UserFactory)
    message = factory.lazy_attribute(
        lambda o: fake.paragraph(nb_sentences=3, variable_nb_sentences=False)
    )
