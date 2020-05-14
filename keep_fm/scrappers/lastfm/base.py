from keep_fm.scrappers.base import Scrapper
from keep_fm.users.models import User


class LastFmScrapper(Scrapper):
    REQUIRED_DATA = ("lastfm_username", "user_id", "url")

    def setup(self, lastfm_username, **kwargs):
        super().setup(**kwargs)
        self.lastfm_username = lastfm_username
        self.user_id = User.objects.get(lastfm_username=self.lastfm_username).id
