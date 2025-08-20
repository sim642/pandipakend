import requests
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape(term):
    logger.info("scrape %s", term)
    result = requests.get(f"https://eestipandipakend.ee/api/package-registry/{term}").json()
    time.sleep(1.0)
    if len(result) < 10:
        for package in result:
            print(package)
    else:
        for digit in range(0, 10):
            scrape(term + str(digit))

scrape("11")
