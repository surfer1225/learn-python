"""Majority Element
https://leetcode.com/problems/majority-element/

Tier 2 — good to prepare · Arrays & Hashing

Return the element that appears more than n/2 times. It is guaranteed to exist.

Follow-up: solve it in O(n) time and O(1) space (Boyer-Moore voting).

Example:
    Input:  nums = [2, 2, 1, 1, 1, 2, 2]
    Output: 2

Run: python arrays/tier2/majority_element.py
"""


def majority_element(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert majority_element([3, 2, 3]) == 3
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    assert majority_element([1]) == 1
    print("ok")
