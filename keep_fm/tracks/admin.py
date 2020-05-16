from django.contrib import admin

from keep_fm.tracks.models import Track, Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "artist_id",
    )
    readonly_fields = (
        "spotify_data",
        "spotify_audio_features",
    )
