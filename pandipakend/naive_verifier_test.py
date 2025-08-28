from .mock_database import MockDatabase
from .naive_verifier import NaiveVerifier


def test_11():
    database = MockDatabase("actual-11.jsonl")
    verifier = NaiveVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 1273

def test_all():
    database = MockDatabase("actual.jsonl")
    verifier = NaiveVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 10171
