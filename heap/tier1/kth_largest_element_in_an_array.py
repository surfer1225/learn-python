"""Kth Largest Element in an Array
https://leetcode.com/problems/kth-largest-element-in-an-array/

Tier 1 — must prepare · Heap / Priority Queue

Return the kth largest element (by sorted order, not distinctness).

Sorting is O(n log n); a size-k heap is O(n log k); quickselect averages O(n).
Be ready to compare all three.

Example:
    Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
    Output: 5

Run: python heap/tier1/kth_largest_element_in_an_array.py
"""


def find_kth_largest(nums: list[int], k: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([1], 1) == 1
    print("ok")
