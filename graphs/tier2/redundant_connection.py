"""Redundant Connection
https://leetcode.com/problems/redundant-connection/

Tier 2 — good to prepare · Graphs

A tree had one extra edge added. Return the edge that can be removed so the
result is again a tree; if several qualify, return the last one in the input.

Example:
    Input:  edges = [[1,2],[1,3],[2,3]]
    Output: [2, 3]

Run: python graphs/tier2/redundant_connection.py
"""


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    print("ok")
