import abc
from .package import Package

class AbstractDatabase(abc.ABC):
    @abc.abstractmethod
    def query(self, term: str) -> list[Package]:
        pass
