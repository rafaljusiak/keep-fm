from typing import Any

from keep_fm.scrappers.base import Scrapper
from keep_fm.users.models import User


class LastFmScrapper(Scrapper):
    REQUIRED_DATA = ("lastfm_username", "user_id", "url")
    lastfm_username: str
    user_id: int

    def setup(self, *args: Any, **kwargs: Any) -> None:
        super().setup(*args, **kwargs)
        lastfm_username = kwargs.get("lastfm_username")
        if lastfm_username is None:
            raise ValueError("lastfm_username must be passed with kwargs")
        self.lastfm_username = lastfm_username
        self.user_id = User.objects.get(lastfm_username=self.lastfm_username).id
