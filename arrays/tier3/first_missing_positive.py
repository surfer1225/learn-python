"""First Missing Positive
https://leetcode.com/problems/first-missing-positive/

Tier 3 — prepare if you have time · Arrays & Hashing

Return the smallest missing positive integer. Must run in O(n) time and use
O(1) auxiliary space — the array itself is your hash table.

Example:
    Input:  nums = [3, 4, -1, 1]
    Output: 2

Run: python arrays/tier3/first_missing_positive.py
"""


def first_missing_positive(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert first_missing_positive([1, 2, 0]) == 3
    assert first_missing_positive([3, 4, -1, 1]) == 2
    assert first_missing_positive([7, 8, 9, 11, 12]) == 1
    print("ok")
