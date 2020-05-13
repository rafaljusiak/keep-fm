from keep_fm.scrappers.lastfm.base import LastFmScrapper


class LastFmScrobblesScrapper(LastFmScrapper):
    def setup(self, lastfm_username, **kwargs):
        super().setup(lastfm_username, **kwargs)
        self.url = f"https://www.last.fm/en/user/{self.lastfm_username}/library"
        self.query_string = "?page="
        self.page_number = 1

    def run(self):
        super().run()
        raise NotImplementedError
