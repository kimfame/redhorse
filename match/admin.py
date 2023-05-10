from django.contrib import admin

from match.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sender",
        "receiver",
        "is_liked",
        "is_matched",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["sender"]
