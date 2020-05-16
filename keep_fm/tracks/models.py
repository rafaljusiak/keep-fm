from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from keep_fm.common.models import ModelMixin
from keep_fm.external.spotify.utils import (
    get_track_data,
    get_track_uri,
    get_track_audio_analysis,
    get_track_audio_features,
)


class Artist(ModelMixin, models.Model):
    name = models.CharField(_("Name"), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")


class Track(ModelMixin, models.Model):
    artist = models.ForeignKey(
        "tracks.Artist",
        related_name="tracks",
        on_delete=models.CASCADE,
        verbose_name=_("Artist"),
    )
    name = models.CharField(_("Name"), max_length=1024)
    spotify_uri = models.CharField(
        _("Spotify API URI"), max_length=512, null=True, blank=True
    )

    @cached_property
    def spotify_data(self):
        data = get_track_data(self.name, self.artist.name)
        return data

    @cached_property
    def spotify_audio_analysis(self):
        spotify_uri = self.spotify_uri or get_track_uri(self.name, self.artist.name)
        if spotify_uri:
            data = get_track_audio_analysis(spotify_uri)
            return data
        return None

    @cached_property
    def spotify_audio_features(self):
        spotify_uri = self.spotify_uri or get_track_uri(self.name, self.artist.name)
        if spotify_uri:
            data = get_track_audio_features(spotify_uri)
            return data
        return None

    def set_spotify_uri(self, overwrite=False):
        if not self.spotify_uri or overwrite:
            uri = get_track_uri(self.name, self.artist.name)
            self.spotify_uri = uri
            self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
