from django.contrib import admin

from phone.models import PhoneVerificationHistory, UserPhone


@admin.register(PhoneVerificationHistory)
class PhoneVerificationHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "phone_number",
        "verification_code",
        "is_verified",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["phone_number"]


@admin.register(UserPhone)
class UserPhoneAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "phone_number",
        "updated_at",
        "created_at",
    ]
    list_display_links = ["phone_number"]
