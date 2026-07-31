"""Rotting Oranges
https://leetcode.com/problems/rotting-oranges/

Tier 2 — good to prepare · Graphs

0 is empty, 1 is fresh, 2 is rotten. Each minute, a rotten orange rots its
4-directional fresh neighbours. Return the minutes until none are fresh, or -1.

Multi-source BFS: seed the queue with every rotten orange at once.

Example:
    Input:  [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    Output: 4

Run: python graphs/tier2/rotting_oranges.py
"""


def oranges_rotting(grid: list[list[int]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0
    print("ok")
