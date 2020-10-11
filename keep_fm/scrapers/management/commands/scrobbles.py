from django.core.management import BaseCommand

from keep_fm.scrapers.lastfm.scrobbles import LastFmScrobblesScraper


class Command(BaseCommand):
    """
    Main command that's scraping scrobbles data of the selected account. If a track or
    artist does not exist in the keep.fm database - it creates a new entry. It uses
    a LastFmScrobblesScrapper to retrieve the scrobbles data (from the newest to the oldest
    ones).

    Args:
    --start_page {int}  -> set a starting page from which the scraper will
                           start to scrap scrobbles.

    --max_retries {int} -> how many times scraper should retry to fetch the
                           data in case of asn error (for example - empty page, or
                           bad connection).

    --retry_delay {int} -> how long script should wait before next request to
                           last.fm (in seconds)

    --only_create       -> if it's set, then command stops when it occurs already
                           existing scrobble
    """

    def add_arguments(self, parser):
        parser.add_argument("lastfm_username", type=str)
        parser.add_argument("--start_page", type=int, required=False)
        parser.add_argument("--max_retries", type=int, required=False)
        parser.add_argument("--retry_delay", type=int, required=False)
        parser.add_argument("--only_create", type=bool, required=False)

    def handle(self, *args, **options):
        params = {}
        lastfm_username_param_value = options.get("lastfm_username")
        lastfm_usernames = lastfm_username_param_value.split(",")

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

        for lastfm_username in lastfm_usernames:
            scraper = LastFmScrobblesScraper()
            scraper.setup(lastfm_username=lastfm_username, **params)
            scraper.run()
