from django.contrib import admin

from keep_fm.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "lastfm_username",
    )
