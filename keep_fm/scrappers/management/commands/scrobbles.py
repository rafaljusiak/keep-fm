from django.core.management import BaseCommand

from keep_fm.scrappers.lastfm.scrobbles import LastFmScrobblesScrapper


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("lastfm_username", type=str)

    def handle(self, *args, **options):
        lastfm_username = options.get("lastfm_username")
        scrapper = LastFmScrobblesScrapper()
        scrapper.setup(lastfm_username=lastfm_username)
        scrapper.run()
