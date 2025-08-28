from .database import QueryCountDatabase
from .mock_database import MockDatabase
from .suffix_tree_scraper import SuffixTreeScraper


def test_11():
    database = QueryCountDatabase(MockDatabase("11.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 1273 # 11.txt isn't deduplicated
    assert database.query_count == 11030

def test_all():
    database = QueryCountDatabase(MockDatabase("all-full.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 10171
    assert database.query_count == 73712
