from django.contrib import admin

from basic_profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "uuid",
        "nickname",
        "birthdate",
        "gender",
        "preferred_gender",
        "mbti",
        # "passions",
        "height",
        "religion",
        "smoking_status",
        "drinking_status",
        "location",
        # "bio",
        "is_banned",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["user"]
    filter_horizontal = ["passion"]

    def passions(self, obj):
        return ", ".join([passion.name for passion in obj.passion.all()])
