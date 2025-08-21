import abc

from .database import AbstractDatabase

from .package import PackageDict


class AbstractScraper(abc.ABC):
    database: AbstractDatabase
    packages: PackageDict

    def __init__(self, database: AbstractDatabase):
        super().__init__()
        self.database = database
        self.packages = {}

    @abc.abstractmethod
    def scrape(self, term: str = ""):
        pass
