from django.contrib import admin
from chat_room.models import ChatRoom, ChatRoomMember


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "uuid",
        "member",
        "is_active",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["uuid"]

    def member(self, obj):
        return ", ".join([user.username for user in obj.users.all()])


@admin.register(ChatRoomMember)
class ChatRoomMemberAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "user",
        "is_active",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["user"]
