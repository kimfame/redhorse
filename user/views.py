from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.utils import get_user_object
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
        user = get_user_object(request)

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            context={"user": user},
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        user = get_user_object(request)

        if user.is_active:
            user.is_active = False
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordReset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer
    http_method_names = ["post"]
