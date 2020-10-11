import abc
import time
from typing import Tuple, Any, Optional

import urllib3
from bs4 import BeautifulSoup
from django.conf import settings

from keep_fm.scrapers.exceptions import (
    ScraperSetupException,
    ScraperStop,
    ScraperEmptyPage,
)


class Scraper(abc.ABC):
    """
    Abstract representation of webscraper that can be inherited by other classes.

    Example implementations may be found in a LastFmScrapper and LastFmScrobblesScraper classes.
    """

    # Class attributes that are always required to be not None
    _ALWAYS_REQUIRED: Tuple[str, ...] = ("url",)

    # Class attributes that are required by an implementation to be not None
    # before the scraping is started.
    REQUIRED_DATA: Tuple[str, ...]

    # Allows to make HTTP requests
    http: urllib3.PoolManager

    # Base URL from which scraper should do its job.
    # Example: "https://www.last.fm/"
    url: str

    # Optional query string that's appended to the url. It can be used whan
    # scraper needs to go through some pagination.
    # Example: "?page="
    query_string: Optional[str]

    # If scraper needs to iterate over pagination, this arg holds the current
    # page number.
    page_number: int

    # Defines how many times scraper should retry to fetch the data in case of
    # an error (for example - empty page, or bad connection).
    max_retries: int

    # How many seconds should wait before making next request to the page (in seconds)
    retry_delay: int

    def __init__(self):
        self.http = urllib3.PoolManager()

    @property
    def all_required_data(self) -> Tuple[str, ...]:
        """ Returns a tuple of atrribute names that must have some value """
        return self._ALWAYS_REQUIRED + self.REQUIRED_DATA

    @property
    def is_ready(self) -> bool:
        """
        Returns True if Scraper instance has all required data
        and is ready to start its job.
        """
        return all(
            [
                getattr(self, field_name) is not None
                for field_name in self.all_required_data
            ]
        )

    def setup(self, *args: Any, **kwargs: Any) -> None:
        """
        Setup scraper by providing all required (and optional) kwargs and
        mapping them to attributes.
        """
        self.max_retries = kwargs.get("max_retries", settings.SCRAPPER_MAX_RETRY)
        self.retry_delay = kwargs.get("retry_delay", settings.SCRAPPER_RETRY_DELAY)

    def run(self) -> None:
        """ Main Scraper method, that is processing given page  """
        self.pre_run()
        while True:
            url = self.get_next_url()
            retry = 0
            while retry < self.max_retries:
                try:
                    soup = self.prepare_soup(url)
                    self.process_page(soup)
                    break
                except ScraperEmptyPage:
                    print(
                        f"Invalid selector or found empty page [{retry}/{self.max_retries}]"
                    )
                    self.on_scraper_empty_page()
                    time.sleep(self.retry_delay)
                    retry += 1
                except ScraperStop:
                    print("Scrapper was stopped!")
                    self.on_scraper_stop()
                    retry = self.max_retries
            if retry == self.max_retries:
                print("Finished!")
                self.on_scraper_finish()
                break

    def prepare_soup(self, url: str) -> BeautifulSoup:
        """
        Makes a GET request nad prepares BeautifulSoup object with the
        page content.
        """
        r = self.http.request("GET", url)
        soup = BeautifulSoup(r.data, "html.parser")
        return soup

    def pre_run(self) -> None:
        """ Method running just before the scraper starts to work """
        if not self.is_ready:
            raise ScraperSetupException(
                "Tried to run scraper without setup or setup method is invalid"
            )

        print("Running scraper with following settings:")
        print(f"Max retries: {self.max_retries}")
        print(f"Delay time: {self.retry_delay}s")

    def get_next_url(self) -> str:
        """
        If scraper uses pagination - this method should return the next url
        that will be processed.
        """
        self.page_number += 1
        return f"{self.url}{self.query_string}{self.page_number}"

    def process_page(self, soup: BeautifulSoup) -> None:
        """
        Main logic of page processing. It can be used for example extract data
        from the website, process it, and then save it to the local database.

        It accepts BeautifulSoup object in an argument, that already has prepared
        page content.
        """
        raise NotImplementedError

    def on_scraper_empty_page(self) -> None:
        """ This method is executed when scraper finds an empty page """
        pass

    def on_scraper_stop(self) -> None:
        """ This method is executed when scraper stops due to some condition """
        pass

    def on_scraper_finish(self) -> None:
        """ This method is executed when scraper finishes scraping """
        pass
