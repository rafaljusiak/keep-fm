from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from django.utils import timezone

from keep_fm.scrappers.exceptions import ScrapperEmptyPage, ScrapperStop
from keep_fm.scrobbles.processors import ScrobbleProcessor

from keep_fm.tracks.utils.naming import clean_track_name
from keep_fm.scrappers.lastfm.base import LastFmScrapper


class LastFmScrobblesScrapper(LastFmScrapper):
    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)
        self.url = f"https://www.last.fm/user/{self.lastfm_username}/library"
        self.query_string = "?page="
        self.page_number = kwargs.get("start_page", 1) - 1
        self.only_create = kwargs.get("only_create", False)

    def get_next_url(self) -> str:
        self.page_number += 1
        return f"{self.url}{self.query_string}{self.page_number}"

    def process_page(self, soup: BeautifulSoup) -> None:
        rows = soup.find_all("tr", class_="chartlist-row")
        for row in rows:
            raw_track_name = row.find("td", class_="chartlist-name").find("a").string
            raw_track_artist = (
                row.find("td", class_="chartlist-artist").find("a").string
            )
            raw_timestamp = (
                row.find("td", class_="chartlist-timestamp")
                .find("span")
                .attrs.get("title")
            )

            track_name = clean_track_name(raw_track_name)
            track_artist = self.parse_track_artist(raw_track_artist)
            timestamp = self.parse_timestamp(raw_timestamp)

            _, created = ScrobbleProcessor.process_and_save(
                user_id=self.user_id,
                artist_name=track_artist,
                track_name=track_name,
                timestamp=timestamp,
            )
            if self.only_create and not created:
                raise ScrapperStop
            print(f"[{timestamp}][NEW:{created}] {track_artist} - {track_name}")
        if not len(rows):
            raise ScrapperEmptyPage

    def on_scrapper_finish(self) -> None:
        print(f"Last page: {self.page_number}")

    def parse_track_artist(self, track_artist: str) -> str:
        return track_artist

    def parse_timestamp(self, timestamp: str) -> datetime:
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
