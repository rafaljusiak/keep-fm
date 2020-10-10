from celery import shared_task
from keep_fm.users.models import User

from keep_fm.scrappers.lastfm.scrobbles import LastFmScrobblesScrapper


@shared_task
def scrap_scrobbles() -> None:
    scrapper = LastFmScrobblesScrapper()
    users = User.objects.filter(lastfm_username__isnull=False)
    for user in users:
        scrapper.setup(
            lastfm_username=user.lastfm_username, only_create=True,
        )
        scrapper.run()
