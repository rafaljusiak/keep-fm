from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from keep_fm.common.models import ModelMixin
from keep_fm.scrobbles.querysets import ScrobblesQueryset


class Scrobble(ModelMixin, models.Model):
    """
    Model that represents a Last.fm scrobble.
    In general - it's basically a timestamp of a Track listened by the User.
    """

    objects = ScrobblesQueryset.as_manager()

    user = models.ForeignKey(
        "users.User",
        related_name="scrobbles",
        on_delete=models.CASCADE,
        verbose_name=_("Listener"),
    )
    track = models.ForeignKey(
        "tracks.Track",
        related_name="scrobbles",
        on_delete=models.CASCADE,
        verbose_name=_("Track"),
    )

    # Timestamp of a Scrobble (when exactly the track was scrobbled)
    scrobble_date = models.DateTimeField(
        _("Scrobble date"),
        default=timezone.now,
    )

    def __str__(self) -> str:
        return f"{self.user_id} {self.track_id} {self.created_at}"

    class Meta:
        verbose_name = _("Scrobble")
        verbose_name_plural = _("Scrobbles")
        unique_together = ("user", "track", "scrobble_date")
