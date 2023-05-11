from django.db.models import Subquery
from rest_framework import viewsets, status
from rest_framework.response import Response

from match.models import Match
from match.serializers import MatchSerializer
from user_profile.models import Profile
from user_profile.serializers import OppositeProfileSerializer


class MatchViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user
        profiles = (
            Profile.objects.select_related("user")
            .prefetch_related("passion")
            .filter(
                user__in=Subquery(
                    Match.objects.filter(
                        receiver=user, is_liked=True, is_matched=False
                    ).values("sender")
                )
            )
        )
        serializer = OppositeProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        serializer = MatchSerializer(context={"user": user}, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
