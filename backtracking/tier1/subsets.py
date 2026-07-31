"""Subsets
https://leetcode.com/problems/subsets/

Tier 1 — must prepare · Backtracking

Return all possible subsets (the power set) of an array of distinct integers.

Example:
    Input:  nums = [1, 2, 3]
    Output: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]

Run: python backtracking/tier1/subsets.py
"""


def subsets(nums: list[int]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(s) for s in subsets([1, 2, 3])) == [
        [], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3],
    ]
    assert subsets([]) == [[]]
    print("ok")
