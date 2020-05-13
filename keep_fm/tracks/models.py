from django.db import models
from django.utils.translation import ugettext_lazy as _

from keep_fm.common.models import ModelMixin


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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Track")
        verbose_name_plural = _("Tracks")
