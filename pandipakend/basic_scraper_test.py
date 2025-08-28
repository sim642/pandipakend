from .basic_scraper import BasicScraper
from .database import QueryCountDatabase
from .mock_database import MockDatabase


def test_11():
    database = QueryCountDatabase(MockDatabase("actual-11.jsonl"))
    scraper = BasicScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 1273
    assert database.query_count == 12170

def test_all():
    database = QueryCountDatabase(MockDatabase("actual.jsonl"))
    scraper = BasicScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 10171
    assert database.query_count == 81250
