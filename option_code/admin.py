from django.contrib import admin

from option_code.models import OptionCode, OptionCodeGroup


@admin.register(OptionCodeGroup)
class OptionCodeGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["name"]


@admin.register(OptionCode)
class OptionCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "group", "sub_id", "value"]
    list_display_links = ["value"]
