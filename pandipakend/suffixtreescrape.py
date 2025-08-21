from . import fakedb as db
import logging
import suffix_tree

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

lookups = 0
seen = suffix_tree.Tree()
seen2 = set()

def scrape(term, depth=0):
    logger.debug("%s %s: %d", depth * " ", term, len(seen.find_all(term)))
    if len(seen.find_all(term)) < 10:
        global lookups
        result = db.lookup(term)
        for package in result:
            if package["barcode"] not in seen2:
                seen.add(package["barcode"], package["barcode"])
            seen2.add(package["barcode"])
        logger.info("%s %s: lookup", depth * " ", term)
        lookups += 1
        if len(result) < 10:
            for package in result:
                print(package)
        else:
            for digit in range(0, 10):
                scrape(term + str(digit), depth=depth+1)
    else:
        for digit in range(0, 10):
            scrape(term + str(digit), depth=depth+1)

for digit in range(0, 10):
    scrape(str(digit), depth=1)
print(lookups)
