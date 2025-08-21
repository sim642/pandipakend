import logging
from typing import override

import suffix_tree

from pandipakend.database import AbstractDatabase
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
    def scrape(self, term: str = ""):
        def scrape(term, depth=0):
            logger.debug("%s %s: %d", depth * " ", term, len(self.barcode_tree.find_all(term)))
            if len(self.barcode_tree.find_all(term)) < 10:
                result = self.database.query(term)
                for package in result:
                    if package["barcode"] not in self.packages:
                        self.barcode_tree.add(package["barcode"], package["barcode"])
                        self.packages[package["barcode"]] = package
                logger.info("%s %s: lookup", depth * " ", term)
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    database = QueryCountDatabase(MockDatabase("11.txt"))
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    print(database.query_count)
    print(len(scraper.packages))
