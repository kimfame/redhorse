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

from phone.views import send_verification_code, verify_verification_code
from user.views import UserViewSet, reset_password
from user_profile.views import MyProfileViewSet, OppositeProfileViewSet
from common_code.views import (
    GenderList,
    PreferredGenderList,
    MBTIList,
    DrinkingStatusList,
    ReligionList,
    LocationList,
)
from passion.views import PassionViewSet
from profile_picture.views import ProfilePictureViewSet
from match.views import MatchViewSet, CountingLike
from chat_room.views import ChatRoomViewSet
from chat_message.views import ChatMessageViewSet
from feed.views import Feed

user_detail = UserViewSet.as_view(
    {
        "post": "create",
        "delete": "destroy",
    }
)
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
chat_room_out = ChatRoomViewSet.as_view({"patch": "partial_update"})

chat_message_list = ChatMessageViewSet.as_view({"get": "list"})
chat_message_create = ChatMessageViewSet.as_view({"post": "create"})

router = DefaultRouter()
router.register("passions", PassionViewSet, basename="passion")
router.register("match", MatchViewSet, basename="match")

urlpatterns = [
    path("", include(router.urls)),
    path("phone/send-code/", send_verification_code),
    path("phone/verify/", verify_verification_code),
    path("users/", user_detail),
    path("users/change-password/", change_password),
    path("users/reset-password/", reset_password),
    path("users/me/profile/", my_profile_detail),
    path("users/<uuid:uuid>/profile", opposite_profile_detail),
    path("users/me/profile-pictures/", profile_picture_list),
    path("users/me/profile-pictures/<uuid:uuid>/", profile_picture_detail),
    path("match/", match_create),
    path("match/received-likes", match_received_likes),
    path("match/remaining-like-num", CountingLike.as_view()),
    path("chats", chat_room_list),
    path("chats/<uuid:uuid>", chat_room_detail),
    path("chats/<uuid:uuid>/messages", chat_message_list),
    path("chats/<uuid:uuid>/messages/", chat_message_create),
    path("chats/<uuid:uuid>/out/", chat_room_out),
    path("feed", Feed.as_view()),
    path("genders", GenderList.as_view()),
    path("preferred-genders", PreferredGenderList.as_view()),
    path("mbti-types", MBTIList.as_view()),
    path("drinking-status", DrinkingStatusList.as_view()),
    path("religions", ReligionList.as_view()),
    path("locations", LocationList.as_view()),
]


if settings.DEBUG:
    urlpatterns += [
        path("admin/", admin.site.urls),
        path("__debug__/", include("debug_toolbar.urls")),
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
