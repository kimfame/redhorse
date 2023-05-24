from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    PasswordResetSerializer,
)


class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()

            refresh = RefreshToken.for_user(new_user)
            token = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(token, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            context={"user": request.user},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        user = request.user

        if user.is_active:
            user.is_active = False
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
