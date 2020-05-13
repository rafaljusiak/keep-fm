from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScrobblesAppConfig(AppConfig):
    name = "keep_fm.scrobbles"
    verbose_name = _("Scrobbles")
