from typing import Any, Dict, Optional

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from keep_fm.common.models import ModelMixin
from keep_fm.external.spotify.processors import map_track_data, map_track_features_data
from keep_fm.external.spotify.utils import (
    get_track_data,
    get_track_uri,
    get_track_audio_analysis,
    get_track_audio_features,
)
from keep_fm.tracks.slugs import slugify_track


class Artist(ModelMixin, models.Model):
    """Model that represents an artist performing a songs (Tracks)"""

    # Name of the artist
    name = models.CharField(_("Name"), max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")


class Track(ModelMixin, models.Model):
    """Model of a song"""

    # Artist that performs the track
    artist = models.ForeignKey(
        "tracks.Artist",
        related_name="tracks",
        on_delete=models.CASCADE,
        verbose_name=_("Artist"),
    )

    # Name of the song
    name = models.CharField(_("Name"), max_length=1024)

    # Slug of the song (artist + track name). It's used mostly in filtering to remove
    # duplicated tracks, like when the case is different between scrobbles.
    # Example: "Take Me Out" and "Take me out"
    slug = models.SlugField(null=True, blank=True, max_length=2048)

    # URL to the track in Spotify
    spotify_uri = models.CharField(
        _("Spotify API URI"), max_length=512, null=True, blank=True
    )

    @cached_property
    def spotify_data(self) -> Optional[Dict[str, Any]]:
        """Data about this track got from Spotify API"""
        data = get_track_data(self.name, self.artist.name)
        if data:
            data = map_track_data(data)
        return data

    @cached_property
    def spotify_audio_analysis(self) -> Optional[Dict[str, Any]]:
        """Data about audio analysis got from Spotify API"""
        spotify_uri = self.spotify_uri or get_track_uri(self.name, self.artist.name)
        if spotify_uri:
            data = get_track_audio_analysis(spotify_uri)
            return data
        return None

    @cached_property
    def spotify_audio_features(self) -> Optional[Dict[str, Any]]:
        """Data about audio features got from Spotify API"""
        spotify_uri = self.spotify_uri or get_track_uri(self.name, self.artist.name)
        if spotify_uri:
            data = get_track_audio_features(spotify_uri)
            if data:
                data = map_track_features_data(data)
            return data
        return None

    def set_spotify_uri(self, overwrite: bool = False) -> None:
        """Sets spotify_uri and saves the Track. It's not overwriting by default"""
        if not self.spotify_uri or overwrite:
            uri = get_track_uri(self.name, self.artist.name)
            self.spotify_uri = uri
            self.save()

    def set_slug(self, overwrite: bool = False) -> None:
        """Generates slug if it's not set. With overwrite=True it's re-generating a slug"""
        if not self.slug or overwrite:
            self.slug = slugify_track(self.artist.name, self.name)
            self.save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
