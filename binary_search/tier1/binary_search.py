"""Binary Search
https://leetcode.com/problems/binary-search/

Tier 1 — must prepare · Binary Search

Search a sorted array for `target` and return its index, or -1. O(log n).

Get the loop invariant right here and every other binary search gets easier.

Example:
    Input:  nums = [-1, 0, 3, 5, 9, 12], target = 9
    Output: 4

Run: python binary_search/tier1/binary_search.py
"""


def search(nums: list[int], target: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert search([5], 5) == 0
    assert search([], 1) == -1
    print("ok")
