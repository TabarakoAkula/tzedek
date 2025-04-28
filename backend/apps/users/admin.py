from django.contrib import admin
from apps.users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "created_at")
    search_fields = ("telegram_id", "username")
    list_filter = ("created_at",)
