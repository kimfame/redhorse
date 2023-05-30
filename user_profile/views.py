from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.utils import get_user_object
from profile_picture.models import ProfilePicture
from user_profile.models import Profile
from user_profile.serializers import (
    MyProfileSerializer,
    OppositeProfileSerializer,
    CreateMyProfileSerializer,
    UpdateMyProfileSerializer,
)


class MyProfileViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = CreateMyProfileSerializer(
            data=request.data,
            context={
                "user": get_user_object(request),
            },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)
        serializer = MyProfileSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request):
        profile = get_object_or_404(Profile, user=request.user.id)

        serializer = UpdateMyProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OppositeProfileViewSet(viewsets.ViewSet):
    def retrieve(self, request, uuid=None):
        profile = get_object_or_404(
            Profile.objects.select_related("user").prefetch_related(
                Prefetch(
                    "user__profilepicture_set",
                    queryset=ProfilePicture.objects.order_by("-main", "id"),
                    to_attr="profile_pictures",
                ),
            ),
            uuid=uuid,
            user__is_active=True,
            is_banned=False,
        )
        serializer = OppositeProfileSerializer(profile)
        return Response(serializer.data)
