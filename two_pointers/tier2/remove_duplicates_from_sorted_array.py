"""Remove Duplicates from Sorted Array
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Tier 2 — good to prepare · Two Pointers

Remove duplicates in place from a sorted array so each element appears once.
Return the new length `k`; the first `k` slots must hold the result.

Example:
    Input:  nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    Output: 5, with nums starting [0, 1, 2, 3, 4]

Run: python two_pointers/tier2/remove_duplicates_from_sorted_array.py
"""


def remove_duplicates(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    nums = [1, 1, 2]
    assert remove_duplicates(nums) == 2
    assert nums[:2] == [1, 2]
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    assert remove_duplicates(nums) == 5
    assert nums[:5] == [0, 1, 2, 3, 4]
    print("ok")
