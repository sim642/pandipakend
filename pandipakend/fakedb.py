import json

db = {}

with open("11.txt", "r") as fd:
    for line in fd:
        package = json.loads(line)
        db[package["barcode"]] = package

def lookup(term: str) -> list[str]:
    return [package for barcode, package in db.items() if term in barcode][:10]

