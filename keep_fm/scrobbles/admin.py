from django.contrib import admin

from keep_fm.scrobbles.models import Scrobble


@admin.register(Scrobble)
class ScrobbleAdmin(admin.ModelAdmin):
    pass
