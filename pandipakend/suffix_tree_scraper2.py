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
    term_set: set[str]

    def __init__(self, database: AbstractDatabase):
        super().__init__(database)
        self.barcode_tree = suffix_tree.Tree()
        self.term_set = set()

    @override
    def scrape(self, term: str = ""):
        cache = {}

        def scrape(term, fwd, depth=0):
            logger.debug("%s %s: %d", depth * " ", term, len(self.barcode_tree.find_all(term)))
            if fwd:
                for i in range(len(term) - 1): # TODO: can check better with suffix_tree (matching statistics?)
                    # for j in range(i, len(term)):
                    j = len(term) - 1 # no point in checking others, they would've been rejected at upper scrape depths
                    if term[i:j] in self.term_set:
                        logger.debug("skipping %s %s", term, term[i:j])
                        return
            else:
                for j in range(2, len(term)): # TODO: can check better with suffix_tree (matching statistics?)
                    # for j in range(i, len(term)):
                    i = 1 # no point in checking others, they would've been rejected at upper scrape depths
                    if term[i:j] in self.term_set:
                        logger.debug("skipping %s %s", term, term[i:j])
                        return
            # need fwd=False, because if term is at end, then extending fwd will not find
            if len(self.barcode_tree.find_all(term)) < 10:
                if term in cache:
                    logger.debug("cached %s", term)
                    result = cache[term]
                else:
                    result = self.database.query(term)
                    cache[term] = result
                for package in result:
                    if package["barcode"] not in self.packages:
                        self.barcode_tree.add(package["barcode"], package["barcode"])
                        self.packages[package["barcode"]] = package
                        print(json.dumps(package, ensure_ascii=False))
                # logger.info("%s %s: lookup", depth * " ", term)
                if len(result) >= 10:
                    for digit in range(0, 10):
                        if fwd:
                            scrape(term + str(digit), fwd, depth=depth+1)
                        else:
                            scrape(str(digit) + term, fwd, depth=depth+1)
            else:
                for digit in range(0, 10):
                    if fwd:
                        scrape(term + str(digit), fwd, depth=depth+1)
                    else:
                        scrape(str(digit) + term, fwd, depth=depth+1)
            self.term_set.add(term)

        if term == "":
            for digit in range(0, 10):
                scrape(str(digit), True, depth=1)
            self.term_set = set()
            for digit in range(0, 10):
                scrape(str(digit), False, depth=1)
        else:
            scrape(term, True)
            self.term_set = set()
            scrape(term, False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # database = QueryCountDatabase(MockDatabase("11.txt"))
    # database = QueryCountDatabase(RealDatabase())
    database = QueryCountDatabase(MockDatabase("all-full.txt")) # TODO: broken
    scraper = SuffixTreeScraper(database)
    scraper.scrape("")
    logger.info("queries: %d", database.query_count)
    logger.info("packages: %d", len(scraper.packages))
