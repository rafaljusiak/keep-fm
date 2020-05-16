from django.contrib import admin

from keep_fm.scrobbles.models import Scrobble


@admin.register(Scrobble)
class ScrobbleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "track",
        "scrobble_date",
    )
    list_select_related = (
        "track",
        "user",
    )
    autocomplete_fields = (
        "track",
        "user",
    )
