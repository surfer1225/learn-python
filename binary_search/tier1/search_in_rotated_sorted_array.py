"""Search in Rotated Sorted Array
https://leetcode.com/problems/search-in-rotated-sorted-array/

Tier 1 — must prepare · Binary Search

A sorted array of distinct values was rotated at an unknown pivot. Find
`target` in O(log n), or return -1.

At every step one half is sorted. Which one, and is the target inside it?

Example:
    Input:  nums = [4, 5, 6, 7, 0, 1, 2], target = 0
    Output: 4

Run: python binary_search/tier1/search_in_rotated_sorted_array.py
"""


def search(nums: list[int], target: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search([1], 0) == -1
    print("ok")
