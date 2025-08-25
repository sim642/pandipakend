from .mock_database import MockDatabase

import suffix_tree
import suffix_tree.node
import suffix_tree.util

database = MockDatabase("all-full.txt")

barcode_tree = suffix_tree.Tree()
for barcode in database.packages.keys():
    barcode_tree.add(barcode, barcode)

barcode_tree.root.compute_C() # not efficient

# print(len(database.packages))

packages = set()

def traverse(node: suffix_tree.node.Node) -> None:
    if isinstance(node, suffix_tree.node.Leaf):
        print(node)
        suffix = "".join(node.S[node.start:node.end - 1])
        for package in database.query(suffix):
            packages.add(package["barcode"])
        pass
    elif isinstance(node, suffix_tree.node.Internal):
        if node.C < 10:
            print(node)
            suffix = "".join(node.S[node.start:node.end])
            for package in database.query(suffix):
                packages.add(package["barcode"])
        else:
            for c, child in node.children.items():
                if isinstance(c, suffix_tree.util.UniqueEndChar):
                    continue
                traverse(child)
    else:
        raise RuntimeError(node)


small_queries: dict[str, set[str]] = {}

def generate(node: suffix_tree.node.Node) -> None:
    if isinstance(node, suffix_tree.node.Leaf):
        print(node)
        suffix = "".join(node.S[node.start:node.end - 1])
        small_queries[suffix] = {id for id, _ in node.get_positions()}
    elif isinstance(node, suffix_tree.node.Internal):
        # if node.C < 10:
        if node.C <= 10: # equality is fine here because we just want to see all, when not confirming exhaustiveness
            print(node)
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
print(len(small_queries))

# very naive greedy set cover
covered = set()
queries = []
while len(covered) < len(database.packages):
    query, s = max(small_queries.items(), key=lambda p: len(p[1] - covered))
    queries.append(query)
    print(query, len(s - covered), s)
    covered.update(s)

print(len(queries))

# traverse(barcode_tree.root)
# print(len(packages))
# print(database.packages.keys() - packages)
