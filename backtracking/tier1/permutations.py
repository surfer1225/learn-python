"""Permutations
https://leetcode.com/problems/permutations/

Tier 1 — must prepare · Backtracking

Return all permutations of an array of distinct integers.

Example:
    Input:  nums = [1, 2, 3]
    Output: 6 permutations

Run: python backtracking/tier1/permutations.py
"""


def permute(nums: list[int]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(permute([1, 2, 3])) == [
        [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1],
    ]
    assert permute([1]) == [[1]]
    print("ok")
