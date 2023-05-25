from django.db.models import Prefetch, Subquery
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import get_remaining_like_num, get_user_object_with_profile
from match.models import Match
from match.serializers import MatchSerializer
from profile_picture.models import ProfilePicture
from user_profile.models import Profile
from user_profile.serializers import OppositeProfileSerializer


class CountingLike(APIView):
    def get(self, request):
        user_id = request.user.id
        like_num = get_remaining_like_num(user_id)
        return Response({"like_num": like_num})


class MatchViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.user.id

        remaining_like = get_remaining_like_num(user_id)
        profile_num = remaining_like if remaining_like > 0 else 1

        profiles = (
            Profile.objects.select_related("user")
            .prefetch_related(
                "passions",
                Prefetch(
                    "user__profilepicture_set",
                    queryset=ProfilePicture.objects.order_by("-main", "id"),
                    to_attr="profile_pictures",
                ),
            )
            .filter(
                user__is_active=True,
                is_banned=False,
                user__in=Subquery(
                    Match.objects.filter(
                        receiver=user_id, is_liked=True, is_matched=False
                    )
                    .values("sender")
                    .exclude(
                        sender__in=Subquery(
                            Match.objects.filter(
                                sender=user_id, is_liked=False, is_matched=False
                            ).values("receiver")
                        )
                    )
                ),
            )[:profile_num]
        )

        serializer = OppositeProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user_object_with_profile(request)
        serializer = MatchSerializer(context={"user": user}, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
