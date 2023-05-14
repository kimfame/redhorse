from django.contrib import admin
from chat_room.models import ChatRoom, ChatRoomMember


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        # "member",
        "user_active_status",
        "is_active",
        "uuid",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["uuid"]

    def member(self, obj):
        return ", ".join([user.username for user in obj.users.all()])

    def user_active_status(self, obj):
        room_member_status = []

        members = ChatRoomMember.objects.select_related("user__profile").filter(
            room=obj
        )

        for member in members:
            room_member_status.append((member.user.profile.nickname, member.is_active))

        return ", ".join(
            [
                f"{member[0]} ({'O' if member[1] else 'X'})"
                for member in room_member_status
            ]
        )


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
