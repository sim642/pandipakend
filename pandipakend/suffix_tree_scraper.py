import json
import logging
from typing import override

import suffix_tree

from pandipakend.database import AbstractDatabase
from pandipakend.real_database import RealDatabase
from pandipakend.scraper import AbstractScraper

from .database import QueryCountDatabase
from .mock_database import MockDatabase


logger = logging.getLogger(__name__)


class SuffixTreeScraper(AbstractScraper):
    barcode_tree: suffix_tree.Tree

    def __init__(self, database: AbstractDatabase):
        super().__init__(database)
        self.barcode_tree = suffix_tree.Tree()

    @override
    def scrape(self, term: str = "", cont=None):
        def scrape(term, depth=0):
            cnt = len(self.barcode_tree.find_all(term))
            # cnt = len(set([i for i, _ in self.barcode_tree.find_all(term)])) # TODO: avoids duplicates, but inefficient
            logger.debug("%s %s: %d", depth * " ", term, cnt)
            if cont is not None:
                if cont.startswith(term):
                    pass
                elif term < cont:
                    return
            if cnt < 10:
                result = self.database.query(term)
                for package in result:
                    if package["barcode"] not in self.packages:
                        self.barcode_tree.add(package["barcode"], package["barcode"])
                        self.packages[package["barcode"]] = package
                        print(json.dumps(package, ensure_ascii=False))
                # logger.info("%s %s: lookup", depth * " ", term)
                if len(result) >= 10:
                    for digit in range(0, 10):
                        scrape(term + str(digit), depth=depth+1)
            else:
                for digit in range(0, 10):
                    scrape(term + str(digit), depth=depth+1)

        if term == "":
            for digit in range(0, 10):
                scrape(str(digit), depth=1)
        else:
            scrape(term)

# TODO: improved version:
# e.g. don't query "10" if all of "0" has been scraped - we have seen everything containing "0", which already includes everything containing "10"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # database = QueryCountDatabase(MockDatabase("11.txt"))
    # database = QueryCountDatabase(RealDatabase())
    database = QueryCountDatabase(MockDatabase("all-full.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    # scraper.scrape("", cont="87659685")
    logger.info("queries: %d", database.query_count)
    logger.info("packages: %d", len(scraper.packages))
