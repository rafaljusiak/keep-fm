from django.contrib import admin

from keep_fm.scrobbles.models import Scrobble


@admin.register(Scrobble)
class ScrobbleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "track",
        "scrobble_date",
    )
