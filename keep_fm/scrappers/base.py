from keep_fm.scrappers.exceptions import ScrapperSetupException


class Scrapper:
    REQUIRED_DATA = ()

    @property
    def is_ready(self):
        return all(
            [getattr(self, field_name) is not None for field_name in self.REQUIRED_DATA]
        )

    def setup(self, **kwargs):
        raise NotImplementedError

    def run(self):
        if not self.is_ready:
            raise ScrapperSetupException(
                "Tried to run scrapper without setup or setup method is invalid"
            )
