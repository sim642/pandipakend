from typing import override

from pandipakend.package import PackageDict

from .verifier import AbstractVerifer


class NaiveVerifier(AbstractVerifer):
    @override
    def verify_queries(self, packages: PackageDict) -> set[str]:
        return set(packages.keys())
