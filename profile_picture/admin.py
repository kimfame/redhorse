from django.contrib import admin
from django.utils.html import format_html

from profile_picture.models import ProfilePicture


@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "main",
        "image_preview",
        "updated_at",
        "created_at",
    )
    list_display_links = ("image_preview",)
    readonly_fields = ("image",)

    def image_preview(self, obj):
        return format_html(
            f"<img src='{obj.image.url}' style='max-width: 200px; max-height: 200px; width: auto; height: auto;'/>"
        )
