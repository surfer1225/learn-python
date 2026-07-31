"""Graph Valid Tree
https://leetcode.com/problems/graph-valid-tree/

Tier 2 — good to prepare · Graphs

Given `n` nodes and an undirected edge list, decide whether the graph forms a
valid tree: fully connected and containing no cycle.

A tree on n nodes has exactly n - 1 edges — that check plus connectivity is
enough. Union-Find is the other standard answer.

Example:
    Input:  n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
    Output: True

Run: python graphs/tier2/graph_valid_tree.py
"""


def valid_tree(n: int, edges: list[list[int]]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True
    assert valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False
    assert valid_tree(1, []) is True
    print("ok")
