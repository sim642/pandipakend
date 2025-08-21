import json
from typing import override

from .database import AbstractDatabase
from .package import Package, PackageDict


class MockDatabase(AbstractDatabase):
    packages: PackageDict

    def __init__(self, filename: str):
        self.load(filename)

    def load(self, filename):
        self.packages = {}
        with open(filename, "r", encoding="utf-8") as fd:
            for line in fd:
                package: Package = json.loads(line)
                self.packages[package["barcode"]] = package

    @override
    def query(self, term: str) -> list[Package]:
        return [package for barcode, package in self.packages.items() if term in barcode][:10]
