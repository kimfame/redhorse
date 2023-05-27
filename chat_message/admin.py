from django.contrib import admin

from chat_message.models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "user",
        # "message",
        "message_summary",
        "updated_datetime",
        "created_datetime",
    ]
    list_display_links = ["id", "message_summary"]

    def message_summary(self, obj):
        return obj.message[:20] if obj.message else None
