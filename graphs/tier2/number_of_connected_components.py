"""Number of Connected Components
https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

Tier 2 — good to prepare · Graphs

Count the connected components in an undirected graph of `n` nodes.

The cleanest Union-Find warm-up; also solvable with DFS.

Example:
    Input:  n = 5, edges = [[0,1],[1,2],[3,4]]
    Output: 2

Run: python graphs/tier2/number_of_connected_components.py
"""


def count_components(n: int, edges: list[list[int]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    assert count_components(3, []) == 3
    print("ok")
