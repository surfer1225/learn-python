"""Unique Paths
https://leetcode.com/problems/unique-paths/

Tier 2 — good to prepare · Dynamic Programming

A robot at the top-left of an m x n grid may move only right or down. How many
distinct paths reach the bottom-right?

Example:
    Input:  m = 3, n = 7
    Output: 28

Run: python dynamic_programming/tier2/unique_paths.py
"""


def unique_paths(m: int, n: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
    assert unique_paths(1, 1) == 1
    print("ok")
