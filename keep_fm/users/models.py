from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from keep_fm.common.models import ModelMixin


class User(ModelMixin, AbstractUser):
    """Application User"""

    objects: UserManager = UserManager()

    # Tracks listened by this User. It uses scrobbles.Scrobble to hold information
    # about "when" a certain track was heard by the User.
    tracks = models.ManyToManyField(
        "tracks.Track", related_name="listeners", through="scrobbles.Scrobble"
    )

    # Name of the user in the http://www.last.fm/
    lastfm_username = models.CharField(
        _("Last.fm Username"), null=True, blank=True, max_length=128
    )
