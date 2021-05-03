# mypy: ignore-errors

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from keep_fm.users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "lastfm_username",
    )

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Configuration", {"fields": ("lastfm_username",)}),
    )
