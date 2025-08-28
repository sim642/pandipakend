from .mock_database import MockDatabase
from .suffix_tree_set_cover_verifier import SuffixTreeSetCoverVerifier


def test_11():
    database = MockDatabase("11.txt")
    verifier = SuffixTreeSetCoverVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 246

def test_all():
    database = MockDatabase("all-full.txt")
    verifier = SuffixTreeSetCoverVerifier()
    queries = verifier.verify_queries(database.packages)
    assert len(queries) == 2159
