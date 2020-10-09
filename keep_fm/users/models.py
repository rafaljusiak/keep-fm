from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from keep_fm.common.models import ModelMixin


class User(ModelMixin, AbstractUser):
    objects: UserManager = UserManager()

    tracks = models.ManyToManyField(
        "tracks.Track", related_name="listeners", through="scrobbles.Scrobble"
    )
    lastfm_username = models.CharField(
        _("Last.fm Username"), null=True, blank=True, max_length=128
    )
