from django.contrib import admin

from user_profile.models import Profile


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
        "passion",
        "height",
        "religion",
        "smoking_status",
        "drinking_status",
        "location",
        # "bio",
        "is_banned",
        "updated_datetime",
        "created_datetime",
    ]
    list_display_links = ["user"]
    filter_horizontal = ["passions"]

    def passion(self, obj):
        return ", ".join([passion.name for passion in obj.passions.all()])
