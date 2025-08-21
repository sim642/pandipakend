from typing import TypedDict


class Package(TypedDict):
    barcode: str
    barcode_type: str
    product_name: str
    package_capacity: int
    product_category: str
    package_type: str
    deposit_fee: str


PackageDict = dict[str, Package]
