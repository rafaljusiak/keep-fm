from typing import Any

from keep_fm.scrapers.base import Scraper
from keep_fm.users.models import User


class LastFmScraper(Scraper):
    """
    Base LastFm scraper that can be used to scrap data from this page.
    It adds a requirement for giving a last.fm user name, and User id from the
    keep.fm database to properly extract and process data, and then
    save it to the local database.
    """

    REQUIRED_DATA = ("lastfm_username", "user_id")

    # User's last.fm username
    lastfm_username: str

    # Id of User instance in the database
    user_id: int

    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)
        lastfm_username = kwargs.get("lastfm_username")
        if lastfm_username is None:
            raise ValueError("lastfm_username must be passed with kwargs")
        self.lastfm_username = lastfm_username
        self.user_id = User.objects.get(lastfm_username=self.lastfm_username).id
