from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from phone.views import VerificationCodeSender, CodeVerification
from user.views import UserViewSet, PasswordReset
from user_profile.views import MyProfileViewSet, OppositeProfileViewSet
from option_code.views import (
    GenderList,
    PreferredGenderList,
    MBTIList,
    DrinkingStatusList,
    ReligionList,
    LocationList,
)
from profile_picture.views import ProfilePictureViewSet
from match.views import MatchViewSet, CountingLike
from chat_room.views import ChatRoomViewSet
from chat_message.views import ChatMessageListViewSet, CreateChatMessage
from feed.views import Feed

user_create = UserViewSet.as_view({"post": "create"})
user_delete = UserViewSet.as_view({"delete": "destroy"})

change_password = UserViewSet.as_view({"patch": "partial_update"})
my_profile_detail = MyProfileViewSet.as_view(
    {
        "post": "create",
        "get": "retrieve",
        "patch": "partial_update",
    }
)
opposite_profile_detail = OppositeProfileViewSet.as_view({"get": "retrieve"})

profile_picture_list = ProfilePictureViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
profile_picture_detail = ProfilePictureViewSet.as_view(
    {
        "patch": "partial_update",
        "delete": "destroy",
    }
)

match_create = MatchViewSet.as_view({"post": "create"})
match_received_likes = MatchViewSet.as_view({"get": "list"})

chat_room_list = ChatRoomViewSet.as_view({"get": "list"})
chat_room_detail = ChatRoomViewSet.as_view({"get": "retrieve"})
chat_room_leave = ChatRoomViewSet.as_view({"patch": "partial_update"})

chat_message_list = ChatMessageListViewSet.as_view({"get": "list"})

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("phone/send-code/", VerificationCodeSender.as_view(), name="send_code"),
    path("phone/verify/", CodeVerification.as_view(), name="verify_code"),
    path("users/", user_create, name="create_user"),
    path("users/me", user_delete, name="delete_user"),
    path("users/change-password/", change_password, name="change_password"),
    path("users/reset-password/", PasswordReset.as_view(), name="reset_password"),
    path("users/me/profile/", my_profile_detail, name="my_profile"),
    path("users/<uuid:uuid>/profile", opposite_profile_detail, name="opposite_profile"),
    path(
        "users/me/profile-pictures/", profile_picture_list, name="profile_picture_list"
    ),
    path(
        "users/me/profile-pictures/<uuid:uuid>/",
        profile_picture_detail,
        name="profile_picture_detail",
    ),
    path("match/", match_create, name="match_create"),
    path("match/received-likes", match_received_likes, name="match_received_likes"),
    path("match/remaining-like-num", CountingLike.as_view(), name="remaining_like_num"),
    path("chats", chat_room_list, name="chat_room_list"),
    path("chats/<uuid:uuid>", chat_room_detail, name="chat_room_detail"),
    path("chats/<uuid:uuid>/messages", chat_message_list, name="chat_message_list"),
    path(
        "chats/<uuid:uuid>/messages/",
        CreateChatMessage.as_view(),
        name="chat_message_create",
    ),
    path("chats/<uuid:uuid>/leave/", chat_room_leave, name="chat_room_leave"),
    path("feed", Feed.as_view(), name="feed"),
    path("genders", GenderList.as_view(), name="gender_list"),
    path(
        "preferred-genders", PreferredGenderList.as_view(), name="preferred_gender_list"
    ),
    path("mbti-types", MBTIList.as_view(), name="mbti_list"),
    path("drinking-status", DrinkingStatusList.as_view(), name="drinking_status_list"),
    path("religions", ReligionList.as_view(), name="religion_list"),
    path("locations", LocationList.as_view(), name="location_list"),
]


if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
    ]
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)),
else:
    urlpatterns.append(path(settings.ADMIN_URL, admin.site.urls))


# Simple JWT
urlpatterns += [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
