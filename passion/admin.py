from django.contrib import admin

from passion.models import Passion


@admin.register(Passion)
class PassionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
