from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from profile_picture.models import ProfilePicture
from profile_picture.serializers import ProfilePictureSerializer


class ProfilePictureViewSet(viewsets.ViewSet):
    def list(self, request):
        profile_pictures = ProfilePicture.objects.filter(user=request.user.id).order_by(
            "-main", "id"
        )
        serializer = ProfilePictureSerializer(profile_pictures, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = request.user.id
        serializer = ProfilePictureSerializer(
            context={"user_id": user_id},
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, uuid=None):
        user_id = request.user.id
        profile_picture = get_object_or_404(ProfilePicture, uuid=uuid, user=user_id)
        serializer = ProfilePictureSerializer(
            profile_picture,
            data=request.data,
            context={"user_id": user_id},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, uuid=None):
        user_id = request.user.id
        if ProfilePicture.objects.filter(uuid=uuid, user=user_id).exists() is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profile_pictures = ProfilePicture.objects.filter(user=user_id).order_by(
            "-main", "id"
        )[:2]

        if len(profile_pictures) < 2:
            return Response(
                {"image": ["프로필 사진은 최소 1장 이상 등록되어야 합니다."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for profile_picture in profile_pictures:
            if profile_picture.uuid == uuid:
                profile_picture.delete()
            elif profile_picture.main == False:
                profile_picture.main = True
                profile_picture.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
