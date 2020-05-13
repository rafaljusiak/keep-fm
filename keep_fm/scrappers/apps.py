from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScrappersAppConfig(AppConfig):
    name = "keep_fm.scrappers"
    verbose_name = _("Scrappers")
