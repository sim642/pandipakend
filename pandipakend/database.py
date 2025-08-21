import abc
from typing import override

from .package import Package


class AbstractDatabase(abc.ABC):
    @abc.abstractmethod
    def query(self, term: str) -> list[Package]:
        pass

class DelegateDatabase(AbstractDatabase):
    delegate: AbstractDatabase

    def __init__(self, delegate: AbstractDatabase):
        super().__init__()
        self.delegate = delegate

    @override
    def query(self, term: str) -> list[Package]:
        return self.delegate.query(term)

class QueryCountDatabase(DelegateDatabase):
    query_count: int

    def __init__(self, delegate: AbstractDatabase):
        super().__init__(delegate)
        self.query_count = 0

    def query(self, term: str) -> list[Package]:
        self.query_count += 1
        return super().query(term)
