from celery import shared_task
from keep_fm.users.models import User

from keep_fm.scrapers.lastfm.scrobbles import LastFmScrobblesScraper


@shared_task
def scrap_scrobbles() -> None:
    """
    Celery periodic task that is fetching newest scrobbles of all Users saved
    in the local database.
    """
    scraper = LastFmScrobblesScraper()
    users = User.objects.filter(lastfm_username__isnull=False)
    for user in users:
        scraper.setup(
            lastfm_username=user.lastfm_username,
            only_create=True,
        )
        scraper.run()
