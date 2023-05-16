from django.db.models import F, Prefetch, Subquery
from rest_framework.views import APIView
from rest_framework.response import Response


from match.models import Match
from profile_picture.models import ProfilePicture
from user_profile.serializers import OppositeProfileSerializer
from user_profile.models import Profile


class Feed(APIView):
    def get(self, request):
        user = request.user
        preferred_gender = user.profile.preferred_gender
        target_gender = ["M", "F"] if preferred_gender == "A" else [preferred_gender]

        match_sender_me = (
            Match.objects.filter(sender=user)
            .annotate(user=F("receiver"))
            .values("user")
        )
        match_receiver_me = (
            Match.objects.filter(receiver=user)
            .annotate(user=F("sender"))
            .values("user")
        )

        profiles = (
            Profile.objects.select_related("user")
            .filter(gender__in=target_gender)
            .exclude(
                user__in=Subquery(
                    match_sender_me.union(match_receiver_me).values("user")
                )
            )
            .exclude(id=user.profile.id)
            .prefetch_related(
                "passion",
                Prefetch(
                    "profilepicture_set",
                    queryset=ProfilePicture.objects.order_by("-main", "id"),
                    to_attr="profile_pictures",
                ),
            )
            .order_by("-id")
        )

        serializer = OppositeProfileSerializer(profiles, many=True)
        return Response(serializer.data)
