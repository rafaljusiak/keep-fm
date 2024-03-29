from datetime import datetime
from typing import Tuple

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from keep_fm.common.models import ModelMixin
from keep_fm.tracks.models import Track


class Scrobble(ModelMixin, models.Model):
    """
    Model that represents a Last.fm scrobble.
    In general - it's basically a timestamp of a Track listened by the User.
    """

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

    @classmethod
    def process_and_save(
        cls, user_id: int, artist_name: str, track_name: str, timestamp: datetime
    ) -> Tuple["Scrobble", bool]:
        """
        All Scrobble objects have to be created with this method to keep them consistent
        in the database.

        Gets or creates Artist and Track records from the local database that are matching
        the given arguments, and then gets or creates a Scrobble object.
        """
        track, _ = Track.process_and_save(artist_name, track_name)

        # Create Scrobble object and associate it with a proper Track and User
        return cls.objects.get_or_create(
            track=track,
            user_id=user_id,
            scrobble_date=timestamp,
        )

    def __str__(self) -> str:
        return f"{self.user_id} {self.track_id} {self.created_at}"

    class Meta:
        verbose_name = _("Scrobble")
        verbose_name_plural = _("Scrobbles")
        unique_together = ("user", "track", "scrobble_date")
