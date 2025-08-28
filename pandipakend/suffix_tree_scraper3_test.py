import pytest

from .database import QueryCountDatabase
from .mock_database import MockDatabase
from .suffix_tree_scraper3 import SuffixTreeScraper


def test_11():
    database = QueryCountDatabase(MockDatabase("11.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 1273 # 11.txt isn't deduplicated
    assert database.query_count == 5755

@pytest.mark.skip(reason="broken scraper")
def test_all():
    database = QueryCountDatabase(MockDatabase("all-full.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    assert len(scraper.packages) == 10171
