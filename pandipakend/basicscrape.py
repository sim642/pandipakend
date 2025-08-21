from . import fakedb as db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

lookups = 0

def scrape(term, depth=0):
    logger.debug("%s %s", depth * " ", term)
    global lookups
    result = db.lookup(term)
    logger.info("%s %s: lookup", depth * " ", term)
    lookups += 1
    if len(result) < 10:
        for package in result:
            print(package)
    else:
        for digit in range(0, 10):
            scrape(term + str(digit), depth=depth+1)

for digit in range(0, 10):
    scrape(str(digit), depth=1)
print(lookups)
