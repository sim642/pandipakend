from .database import QueryCountDatabase
from .mock_database import MockDatabase
from .suffix_tree_scraper import SuffixTreeScraper


def test_11():
    database = QueryCountDatabase(MockDatabase("actual-11.jsonl"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 1273
    assert database.query_count == 11022

def test_all():
    database = QueryCountDatabase(MockDatabase("actual.jsonl"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 10171
    assert database.query_count == 73713
