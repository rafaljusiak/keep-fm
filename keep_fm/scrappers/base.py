import time

import urllib3
from bs4 import BeautifulSoup
from django.conf import settings

from keep_fm.scrappers.exceptions import (
    ScrapperSetupException,
    ScrapperStop,
    ScrapperEmptyPage,
)


class Scrapper:
    _ALWAYS_REQUIRED = ("url",)
    REQUIRED_DATA = ()

    url = None
    query_string = None
    page_number = None
    max_retries = None
    retry_delay = None

    def __init__(self):
        self.http = urllib3.PoolManager()

    @property
    def all_required_data(self):
        return self._ALWAYS_REQUIRED + self.REQUIRED_DATA

    @property
    def is_ready(self):
        return all(
            [
                getattr(self, field_name) is not None
                for field_name in self.all_required_data
            ]
        )

    def setup(self, **kwargs):
        self.max_retries = kwargs.get("max_retries", settings.SCRAPPER_MAX_RETRY)
        self.retry_delay = kwargs.get("retry_delay", settings.SCRAPPER_RETRY_DELAY)

    def get_next_url(self):
        raise NotImplementedError

    def process_page(self, url):
        raise NotImplementedError

    def prepare_soup(self, url):
        r = self.http.request("GET", url)
        soup = BeautifulSoup(r.data, "html.parser")
        return soup

    def pre_run(self):
        if not self.is_ready:
            raise ScrapperSetupException(
                "Tried to run scrapper without setup or setup method is invalid"
            )

        print("Running scrapper with following settings:")
        print(f"Max retries: {self.max_retries}")
        print(f"Delay time: {self.retry_delay}s")

    def run(self):
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

    def on_scrapper_empty_page(self):
        pass

    def on_scrapper_stop(self):
        pass

    def on_scrapper_finish(self):
        pass
