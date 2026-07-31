"""Clone Graph
https://leetcode.com/problems/clone-graph/

Tier 1 — must prepare · Graphs

Return a deep copy of a connected undirected graph. Each node holds a value and
a list of neighbours.

The cycle is the whole problem: you need a visited map from original node to
its copy, and you must consult it *before* recursing.

Example:
    Input:  adjacency = [[2, 4], [1, 3], [2, 4], [1, 3]]
    Output: an identical graph made of new nodes

Run: python graphs/tier1/clone_graph.py
"""


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_graph(adjacency: list[list[int]]) -> Node | None:
    """Build an undirected graph from a 1-indexed adjacency list."""
    if not adjacency:
        return None
    nodes = {i: Node(i) for i in range(1, len(adjacency) + 1)}
    for i, neighbors in enumerate(adjacency, start=1):
        nodes[i].neighbors = [nodes[n] for n in neighbors]
    return nodes[1]


def to_adjacency(node: Node | None) -> list[list[int]]:
    """Flatten a graph back into a 1-indexed adjacency list."""
    if node is None:
        return []
    seen: dict[int, Node] = {}
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.val in seen:
            continue
        seen[cur.val] = cur
        stack.extend(cur.neighbors)
    return [sorted(n.val for n in seen[key].neighbors) for key in sorted(seen)]


def clone_graph(node: Node | None) -> Node | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    adjacency = [[2, 4], [1, 3], [2, 4], [1, 3]]
    original = build_graph(adjacency)
    cloned = clone_graph(original)
    assert to_adjacency(cloned) == adjacency
    assert cloned is not original  # must be new nodes
    assert clone_graph(None) is None
    print("ok")
