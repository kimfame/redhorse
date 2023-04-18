from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = []


if settings.DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(path(settings.ADMIN_URL, admin.site.urls))
