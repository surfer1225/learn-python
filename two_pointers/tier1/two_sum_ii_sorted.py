"""Two Sum II - Input Array Is Sorted
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Tier 1 — must prepare · Two Pointers

The array is sorted in non-decreasing order. Return the 1-indexed positions of
the two numbers adding up to `target`. Use O(1) extra space — so no hash map.

Example:
    Input:  numbers = [2, 7, 11, 15], target = 9
    Output: [1, 2]

Run: python two_pointers/tier1/two_sum_ii_sorted.py
"""


def two_sum(numbers: list[int], target: int) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [1, 2]
    assert two_sum([2, 3, 4], 6) == [1, 3]
    assert two_sum([-1, 0], -1) == [1, 2]
    print("ok")
