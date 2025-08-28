import logging
from typing import override

import suffix_tree
import suffix_tree.node
import suffix_tree.util

from pandipakend.package import PackageDict

from .verifier import AbstractVerifer


logger = logging.getLogger(__name__)


class SuffixTreeSetCoverVerifier(AbstractVerifer):
    @override
    def verify_queries(self, packages: PackageDict) -> set[str]:
        barcode_tree = suffix_tree.Tree()

        for barcode in packages.keys():
            barcode_tree.add(barcode, barcode)

        barcode_tree.root.compute_C() # not efficient


        small_queries: dict[str, set[str]] = {}

        def generate(node: suffix_tree.node.Node) -> None:
            if isinstance(node, suffix_tree.node.Leaf):
                logger.debug("generate %s", node)
                suffix = "".join(node.S[node.start:node.end - 1])
                small_queries[suffix] = {id for id, _ in node.get_positions()}
            elif isinstance(node, suffix_tree.node.Internal):
                if node.C <= 10: # equality is fine here because we just want to see all, when not confirming exhaustiveness
                    logger.debug("generate %s", node)
                    suffix = "".join(node.S[node.start:node.end])
                    small_queries[suffix] = {id for id, _ in node.get_positions()}
                else:
                    for c, child in node.children.items():
                        if isinstance(c, suffix_tree.util.UniqueEndChar):
                            continue
                        generate(child)
            else:
                raise RuntimeError(node)

        generate(barcode_tree.root)


        # very naive greedy set cover
        covered = set()
        queries = set()
        while len(covered) < len(packages):
            query, s = max(small_queries.items(), key=lambda p: len(p[1] - covered))
            queries.add(query)
            logger.debug("cover %s %d %s", query, len(s - covered), s)
            covered.update(s)

        return queries
