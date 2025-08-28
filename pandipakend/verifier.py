import abc

from .package import PackageDict


class AbstractVerifer(abc.ABC):
    @abc.abstractmethod
    def verify_queries(self, packages: PackageDict) -> set[str]:
        pass
