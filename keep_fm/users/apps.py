from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):
    name = "keep_fm.users"
    verbose_name = _("Users")
