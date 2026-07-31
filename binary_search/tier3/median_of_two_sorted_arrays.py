"""Median of Two Sorted Arrays
https://leetcode.com/problems/median-of-two-sorted-arrays/

Tier 3 — prepare if you have time · Binary Search

Return the median of two sorted arrays in O(log(min(m, n))).

Merging is O(m + n) and will be rejected. Binary search the partition point.

Example:
    Input:  nums1 = [1, 2], nums2 = [3, 4]
    Output: 2.5

Run: python binary_search/tier3/median_of_two_sorted_arrays.py
"""


def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert find_median_sorted_arrays([1, 3], [2]) == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4]) == 2.5
    assert find_median_sorted_arrays([], [1]) == 1.0
    print("ok")
