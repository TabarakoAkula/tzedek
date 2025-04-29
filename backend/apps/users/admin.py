from apps.users.models import User
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(User)
class UsersAdmin(ModelAdmin):
    list_display = ("telegram_id", "username", "created_at")
    search_fields = ("telegram_id", "username")
    list_filter = ("created_at",)
