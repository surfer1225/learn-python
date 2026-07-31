"""Merge Sorted Array
https://leetcode.com/problems/merge-sorted-array/

Tier 2 — good to prepare · Arrays & Hashing

`nums1` has length m + n: the first m slots hold its values, the rest are 0.
Merge `nums2` (n values) into `nums1` in place, keeping it sorted.

Hint: filling from the front forces shifting. What if you fill from the back?

Example:
    Input:  nums1 = [1, 2, 3, 0, 0, 0], m = 3, nums2 = [2, 5, 6], n = 3
    Output: [1, 2, 2, 3, 5, 6]

Run: python arrays/tier2/merge_sorted_array.py
"""


def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    nums1 = [1, 2, 3, 0, 0, 0]
    merge(nums1, 3, [2, 5, 6], 3)
    assert nums1 == [1, 2, 2, 3, 5, 6]
    nums1 = [0]
    merge(nums1, 0, [1], 1)
    assert nums1 == [1]
    print("ok")
