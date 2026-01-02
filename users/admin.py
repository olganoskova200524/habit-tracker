from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Telegram", {"fields": ("telegram_chat_id",)}),
    )
    list_display = UserAdmin.list_display + ("telegram_chat_id",)
