import time
from typing import Tuple, Any

import urllib3
from bs4 import BeautifulSoup
from django.conf import settings

from keep_fm.scrappers.exceptions import (
    ScrapperSetupException,
    ScrapperStop,
    ScrapperEmptyPage,
)


class Scrapper:
    _ALWAYS_REQUIRED: Tuple[str, ...] = ("url",)
    REQUIRED_DATA: Tuple[str, ...]

    http: urllib3.PoolManager
    url: str
    query_string: str
    page_number: int
    max_retries: int
    retry_delay: int

    def __init__(self):
        self.http = urllib3.PoolManager()

    @property
    def all_required_data(self) -> Tuple[str, ...]:
        return self._ALWAYS_REQUIRED + self.REQUIRED_DATA

    @property
    def is_ready(self) -> bool:
        return all(
            [
                getattr(self, field_name) is not None
                for field_name in self.all_required_data
            ]
        )

    def setup(self, *args: Any, **kwargs: Any) -> None:
        self.max_retries = kwargs.get("max_retries", settings.SCRAPPER_MAX_RETRY)
        self.retry_delay = kwargs.get("retry_delay", settings.SCRAPPER_RETRY_DELAY)

    def get_next_url(self) -> str:
        raise NotImplementedError

    def process_page(self, url: str) -> None:
        raise NotImplementedError

    def prepare_soup(self, url: str) -> BeautifulSoup:
        r = self.http.request("GET", url)
        soup = BeautifulSoup(r.data, "html.parser")
        return soup

    def pre_run(self) -> None:
        if not self.is_ready:
            raise ScrapperSetupException(
                "Tried to run scrapper without setup or setup method is invalid"
            )

        print("Running scrapper with following settings:")
        print(f"Max retries: {self.max_retries}")
        print(f"Delay time: {self.retry_delay}s")

    def run(self) -> None:
        self.pre_run()
        while True:
            url = self.get_next_url()
            retry = 0
            while retry < self.max_retries:
                try:
                    soup = self.prepare_soup(url)
                    self.process_page(soup)
                    break
                except ScrapperEmptyPage:
                    print(
                        f"Invalid selector or found empty page [{retry}/{self.max_retries}]"
                    )
                    self.on_scrapper_empty_page()
                    time.sleep(self.retry_delay)
                    retry += 1
                except ScrapperStop:
                    print("Scrapper was stopped!")
                    self.on_scrapper_stop()
                    retry = self.max_retries
            if retry == self.max_retries:
                print("Finished!")
                self.on_scrapper_finish()
                break

    def on_scrapper_empty_page(self) -> None:
        pass

    def on_scrapper_stop(self) -> None:
        pass

    def on_scrapper_finish(self) -> None:
        pass
