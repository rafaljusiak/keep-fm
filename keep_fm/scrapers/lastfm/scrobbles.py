from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from django.utils import timezone

from keep_fm.scrapers.exceptions import ScraperEmptyPage, ScraperStop

from keep_fm.scrobbles.models import Scrobble
from keep_fm.tracks.utils.naming import clean_track_name
from keep_fm.scrapers.lastfm.base import LastFmScraper


class LastFmScrobblesScraper(LastFmScraper):
    """
    Scraps scrobbles data from some account and associates them with
    a local user. It also creates artists and tracks if these don't exist
    in the database.
    """

    # Whether only new scrobbles should be saved. If it's True - it stops
    # when scraper finds already existing scrobble.
    only_create: bool

    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)
        self.url = f"https://www.last.fm/user/{self.lastfm_username}/library"
        self.query_string = "?page="
        self.page_number = kwargs.get("start_page", 1) - 1
        self.only_create = kwargs.get("only_create", False)

    def process_page(self, soup: BeautifulSoup) -> None:
        print("Processing next page")
        # Get all rows with scrobbles
        rows = soup.find_all("tr", class_="chartlist-row")

        # Iterate over all rows and extract: track name, artist and scrobble timestamp
        for row in rows:
            print("Processing row ...")
            raw_track_name = row.find("td", class_="chartlist-name").find("a").string
            raw_track_artist = (
                row.find("td", class_="chartlist-artist").find("a").string
            )
            raw_timestamp = (
                row.find("td", class_="chartlist-timestamp")
                .find("span")
                .attrs.get("title")
            )

            # Clean all data and prepare to be saved to db
            track_name = clean_track_name(raw_track_name)
            track_artist = raw_track_artist  # no need to clean this data
            timestamp = self.parse_timestamp(raw_timestamp)

            # Process and save scrobble data
            _, created = Scrobble.process_and_save(
                user_id=self.user_id,
                artist_name=track_artist,
                track_name=track_name,
                timestamp=timestamp,
            )

            # If --only_create flag has been set and scrobble was not created
            # then stop the processing
            if self.only_create and not created:
                raise ScraperStop
            print(f"[{timestamp}][NEW:{created}] {track_artist} - {track_name}")

        # Stop if there's no scrobbles on this page
        if not len(rows):
            raise ScraperEmptyPage

    def on_scraper_finish(self) -> None:
        print(f"Last page: {self.page_number}")

    def parse_timestamp(self, timestamp: str) -> datetime:
        """Parses string timestamp from last.fm and creates adequate datetime object"""
        cleaned = timestamp.replace(",", "").split(" ")
        day = cleaned[1]
        month = timezone.datetime.strptime(cleaned[2], "%b").month
        year = cleaned[3]
        time = timezone.datetime.strptime(cleaned[4], "%I:%M%p")
        hour = time.hour
        minute = time.minute
        parsed = timezone.now().replace(
            day=int(day),
            month=int(month),
            year=int(year),
            hour=int(hour),
            minute=int(minute),
            second=0,
            microsecond=0,
        )
        return parsed
