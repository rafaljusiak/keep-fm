from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ScrappersAppConfig(AppConfig):
    name = "keep_fm.scrapers"
    verbose_name = _("Scrappers")
