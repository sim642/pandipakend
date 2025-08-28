from .mock_database import MockDatabase
from .naive_verifier import NaiveVerifier


def test_11():
    database = MockDatabase("11.txt")
    verifier = NaiveVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 1273 # 11.txt isn't deduplicated

def test_all():
    database = MockDatabase("all-full.txt")
    verifier = NaiveVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 10171
