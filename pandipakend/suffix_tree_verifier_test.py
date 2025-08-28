from .mock_database import MockDatabase
from .suffix_tree_verifier import SuffixTreeVerifier


def test_11():
    database = MockDatabase("actual-11.jsonl")
    verifier = SuffixTreeVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 4000

def test_all():
    database = MockDatabase("actual.jsonl")
    verifier = SuffixTreeVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 29794
