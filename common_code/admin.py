from django.contrib import admin

from common_code.models import CommonCode, CommonCodeGroup


@admin.register(CommonCodeGroup)
class CommonCodeGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]


@admin.register(CommonCode)
class CommonCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "group", "sub_id", "value"]
    list_display_links = ["value"]
