"""Subsets II
https://leetcode.com/problems/subsets-ii/

Tier 2 — good to prepare · Backtracking

Return all possible subsets of an array that may contain duplicates. The result
must not contain duplicate subsets.

Example:
    Input:  nums = [1, 2, 2]
    Output: [[], [1], [1,2], [1,2,2], [2], [2,2]]

Run: python backtracking/tier2/subsets_ii.py
"""


def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(s) for s in subsets_with_dup([1, 2, 2])) == [
        [], [1], [1, 2], [1, 2, 2], [2], [2, 2],
    ]
    assert sorted(subsets_with_dup([0])) == [[], [0]]
    print("ok")
