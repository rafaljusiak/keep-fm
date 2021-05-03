from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TracksAppConfig(AppConfig):
    name = "keep_fm.tracks"
    verbose_name = _("Tracks")
