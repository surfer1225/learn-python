"""Find Minimum in Rotated Sorted Array
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Tier 1 — must prepare · Binary Search

Return the minimum of a rotated sorted array of distinct values, in O(log n).

Example:
    Input:  nums = [4, 5, 6, 7, 0, 1, 2]
    Output: 0

Run: python binary_search/tier1/find_minimum_in_rotated_sorted_array.py
"""


def find_min(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert find_min([3, 4, 5, 1, 2]) == 1
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min([11, 13, 15, 17]) == 11
    print("ok")
