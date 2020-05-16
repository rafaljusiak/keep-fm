from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExternalAppConfig(AppConfig):
    name = "keep_fm.external"
    verbose_name = _("External")
