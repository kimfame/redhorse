from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from phone.views import send_verification_code, verify_verification_code
from user.views import UserViewSet, reset_password
from basic_profile.views import ProfileViewSet

user_detail = UserViewSet.as_view({"post": "create", "delete": "destroy"})
change_password = UserViewSet.as_view({"patch": "partial_update"})
profile_detail = ProfileViewSet.as_view(
    {
        "post": "create",
        "get": "retrieve",
        "patch": "partial_update",
    }
)

urlpatterns = [
    path("phone/send-code/", send_verification_code),
    path("phone/verify/", verify_verification_code),
    path("users/", user_detail),
    path("users/change-password/", change_password),
    path("users/reset-password/", reset_password),
    path("users/me/profile/", profile_detail),
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
