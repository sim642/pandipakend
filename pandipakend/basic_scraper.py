import json
import logging
from typing import override

from pandipakend.real_database import RealDatabase

from .database import QueryCountDatabase
from .mock_database import MockDatabase
from .scraper import AbstractScraper


logger = logging.getLogger(__name__)


class BasicScraper(AbstractScraper):
    @override
    def scrape(self, term: str = ""):
        def scrape(term, depth=0):
            logger.debug("%s %s", depth * " ", term)
            result = self.database.query(term)
            for package in result:
                if package["barcode"] not in self.packages:
                    self.packages[package["barcode"]] = package
                    print(json.dumps(package, ensure_ascii=False))
            # logger.info("%s %s: lookup", depth * " ", term)
            if len(result) >= 10:
                for digit in range(0, 10):
                    scrape(term + str(digit), depth=depth+1)

        if term == "":
            for digit in range(0, 10):
                scrape(str(digit), depth=1)
        else:
            scrape(term)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # database = QueryCountDatabase(MockDatabase("11.txt"))
    database = QueryCountDatabase(RealDatabase())
    scraper = BasicScraper(database)
    scraper.scrape("")
    logger.info("queries: %d", database.query_count)
    logger.info("packages: %d", len(scraper.packages))
