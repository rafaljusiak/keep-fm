from django.utils import timezone

from keep_fm.scrappers.exceptions import ScrapperEmptyPage
from keep_fm.scrobbles.models import Scrobble

from keep_fm.tracks.models import Artist, Track

from keep_fm.common.spotify.naming import REDUNDANT_ENDINGS
from keep_fm.scrappers.lastfm.base import LastFmScrapper


class LastFmScrobblesScrapper(LastFmScrapper):
    def setup(self, lastfm_username, **kwargs):
        super().setup(lastfm_username, **kwargs)
        self.url = f"https://www.last.fm/user/{self.lastfm_username}/library"
        self.query_string = "?page="
        self.page_number = kwargs.get("start_page", 1) - 1

    def get_next_url(self):
        self.page_number += 1
        return f"{self.url}{self.query_string}{self.page_number}"

    def process_page(self, soup):
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

            track_name = self.parse_track_name(raw_track_name)
            track_artist = self.parse_track_artist(raw_track_artist)
            timestamp = self.parse_timestamp(raw_timestamp)

            artist, _ = Artist.objects.get_or_create(name=track_artist)
            track, _ = Track.objects.get_or_create(name=track_name, artist=artist)
            _, created = Scrobble.objects.get_or_create(
                track=track, user_id=self.user_id, scrobble_date=timestamp,
            )
            print(f"[{timestamp}][NEW:{created}] {track_artist} - {track_name}")
        if not len(rows):
            raise ScrapperEmptyPage

    def on_scrapper_finish(self):
        print(f"Last page: {self.page_number}")

    def parse_track_name(self, track_name):
        if "-" in track_name:
            lower_parsed = track_name.lower().split("-")
            if any([ending in lower_parsed[-1] for ending in REDUNDANT_ENDINGS]):
                cleaned_track_name = track_name.rsplit("-", 1)[0]
                if cleaned_track_name[-1] == " ":
                    return cleaned_track_name[:-1]
                return cleaned_track_name
        return track_name

    def parse_track_artist(self, track_artist):
        return track_artist

    def parse_timestamp(self, timestamp):
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
