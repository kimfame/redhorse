from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from profile_picture.models import ProfilePicture
from user_profile.models import Profile
from user_profile.serializers import (
    MyProfileSerializer,
    OppositeProfileSerializer,
    CreateMyProfileSerializer,
    UpdateMyProfileSerializer,
)
from common_code.models import CommonCode


class MyProfileViewSet(viewsets.ViewSet):
    def create(self, request):
        common_code_queryset = self._get_profile_common_code_queryset()

        serializer = CreateMyProfileSerializer(
            data=request.data,
            context={
                "user": request.user,
                "common_code_queryset": common_code_queryset,
            },
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
        profile = get_object_or_404(
            Profile.objects.prefetch_related("passions"),
            user=request.user,
        )
        serializer = MyProfileSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request):
        profile = get_object_or_404(
            Profile.objects.prefetch_related("passions"),
            user=request.user,
        )
        common_code_queryset = self._get_profile_common_code_queryset()

        serializer = UpdateMyProfileSerializer(
            profile,
            data=request.data,
            context={"common_code_queryset": common_code_queryset},
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_profile_common_code_queryset(self) -> QuerySet:
        return CommonCode.objects.select_related("group").filter(
            group__name__in=[
                "gender",
                "preferred_gender",
                "mbti",
                "religion",
                "drinking_status",
                "location",
            ]
        )


class OppositeProfileViewSet(viewsets.ViewSet):
    def retrieve(self, request, uuid=None):
        profile = get_object_or_404(
            Profile.objects.select_related("user").prefetch_related(
                "passions",
                Prefetch(
                    "user__profilepicture_set",
                    queryset=ProfilePicture.objects.order_by("-main", "id"),
                    to_attr="profile_pictures",
                ),
            ),
            uuid=uuid,
        )
        serializer = OppositeProfileSerializer(profile)
        return Response(serializer.data)
