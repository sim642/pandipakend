import time
from typing import override

import requests

from .database import AbstractDatabase
from .package import Package


class RealDatabase(AbstractDatabase):
    @override
    def query(self, term: str) -> list[Package]:
        result = requests.get(f"https://eestipandipakend.ee/api/package-registry/{term}").json()
        time.sleep(1.0) # TODO: where to sleep?
        return result
