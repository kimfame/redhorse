import factory

from factory.django import DjangoModelFactory

from user.factories import UserFactory
from match.models import Match


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)
