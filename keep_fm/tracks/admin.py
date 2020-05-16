from django.contrib import admin

from keep_fm.tracks.models import Track, Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "artist",
        "spotify_uri",
    )
    readonly_fields = (
        "spotify_data",
        "spotify_audio_features",
    )
    list_select_related = ("artist",)
    autocomplete_fields = ("artist",)
    search_fields = (
        "name",
        "artist__name",
    )
