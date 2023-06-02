from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils import get_option_code_list, get_user_object
from profile_picture.models import ProfilePicture
from user_profile import choices
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


class ProfileOption(APIView):
    def get(self, request, option_field_name=None):
        if option_field_name == "genders":
            option_list = {k: v for k, v in choices.Gender.choices}
        elif option_field_name == "preferred-genders":
            option_list = {k: v for k, v in choices.PreferredGender.choices}
        elif option_field_name == "mbti-types":
            option_list = get_option_code_list("mbti")
        elif option_field_name == "drinking-status":
            option_list = [c[0] for c in choices.DrinkingStatus.choices]
        elif option_field_name == "religions":
            option_list = [c[0] for c in choices.Religion.choices]
        elif option_field_name == "locations":
            option_list = [c[0] for c in choices.Location.choices]
        elif option_field_name == "passions":
            option_list = get_option_code_list("passion")
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(option_list)
