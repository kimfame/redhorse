from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import TemporaryPasswordIssueHistory

UserAdmin.ordering = ["-id"]
UserAdmin.list_display = [
    "id",
    "username",
    "is_active",
    "is_staff",
    "is_superuser",
    "date_joined",
]
UserAdmin.list_display_links = ["username"]


@admin.register(TemporaryPasswordIssueHistory)
class TemporaryPasswordIssueHistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_display_links = ["user"]
