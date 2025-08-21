from .database import QueryCountDatabase
from .mock_database import MockDatabase
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

database = QueryCountDatabase(MockDatabase("11.txt"))

def scrape(term, depth=0):
    logger.debug("%s %s", depth * " ", term)
    result = database.query(term)
    logger.info("%s %s: lookup", depth * " ", term)
    if len(result) < 10:
        for package in result:
            print(package)
    else:
        for digit in range(0, 10):
            scrape(term + str(digit), depth=depth+1)

for digit in range(0, 10):
    scrape(str(digit), depth=1)
print(database.query_count)
