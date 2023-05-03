from django.contrib.auth.admin import UserAdmin

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
