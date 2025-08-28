from .basic_scraper import BasicScraper
from .database import QueryCountDatabase
from .mock_database import MockDatabase


def test_11():
    database = QueryCountDatabase(MockDatabase("11.txt"))
    scraper = BasicScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 1273 # 11.txt isn't deduplicated
    assert database.query_count == 12170

def test_all():
    database = QueryCountDatabase(MockDatabase("all-full.txt"))
    scraper = BasicScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 10171
    assert database.query_count == 81250
