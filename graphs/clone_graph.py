"""Clone Graph
https://leetcode.com/problems/clone-graph/

Given a reference of a node in a connected undirected graph, return a deep copy
(clone) of the graph.
"""

from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Optional[Node]) -> Optional[Node]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    a = Node(1)
    b = Node(2)
    a.neighbors = [b]
    b.neighbors = [a]
    cloned = clone_graph(a)
    assert cloned is not a and cloned.val == 1
    print("ok")
