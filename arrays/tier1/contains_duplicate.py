"""Contains Duplicate
https://leetcode.com/problems/contains-duplicate/

Tier 1 — must prepare · Arrays & Hashing

Return `True` if any value appears at least twice in `nums`, and `False` if
every element is distinct.

Example:
    Input:  nums = [1, 2, 3, 1]
    Output: True

Run: python arrays/tier1/contains_duplicate.py
"""


def contains_duplicate(nums: list[int]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert contains_duplicate([1, 2, 3, 1]) is True
    assert contains_duplicate([1, 2, 3, 4]) is False
    assert contains_duplicate([]) is False
    print("ok")
