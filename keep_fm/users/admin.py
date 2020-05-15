from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from keep_fm.users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "lastfm_username",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Configuration", {"fields": ("lastfm_username",)}),
    )
