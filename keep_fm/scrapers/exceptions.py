class ScraperSetupException(Exception):
    """ Invalid Scraper setup """

    pass


class ScraperEmptyPage(Exception):
    """ Scraper found an empty page """

    pass


class ScraperStop(Exception):
    """
    Scraper stopped due to some conition.
    It should be raised manually in a process_page (if needed)
    """

    pass
