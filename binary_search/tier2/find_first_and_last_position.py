"""Find First and Last Position of Element
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/

Tier 2 — good to prepare · Binary Search

Return the first and last index of `target` in a sorted array, or [-1, -1].
Must be O(log n) — so two binary searches, not one plus a scan.

Example:
    Input:  nums = [5, 7, 7, 8, 8, 10], target = 8
    Output: [3, 4]

Run: python binary_search/tier2/find_first_and_last_position.py
"""


def search_range(nums: list[int], target: int) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
    print("ok")
