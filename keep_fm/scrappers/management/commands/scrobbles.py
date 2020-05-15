from django.core.management import BaseCommand

from keep_fm.scrappers.lastfm.scrobbles import LastFmScrobblesScrapper


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("lastfm_username", type=str)
        parser.add_argument("--start_page", type=int, required=False)
        parser.add_argument("--max_retries", type=int, required=False)
        parser.add_argument("--retry_delay", type=int, required=False)
        parser.add_argument("--only_create", type=bool, required=False)

    def handle(self, *args, **options):
        params = {}
        lastfm_username = options.get("lastfm_username")

        start_page = options.get("start_page")
        if start_page:
            params["start_page"] = start_page

        max_retries = options.get("max_retries")
        if max_retries:
            params["max_retries"] = max_retries

        retry_delay = options.get("retry_delay")
        if retry_delay:
            params["retry_delay"] = retry_delay

        only_create = options.get("only_create")
        if only_create:
            params["only_create"] = only_create

        scrapper = LastFmScrobblesScrapper()
        scrapper.setup(lastfm_username=lastfm_username, **params)
        scrapper.run()
