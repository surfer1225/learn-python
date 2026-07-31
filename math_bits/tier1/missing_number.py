"""Missing Number
https://leetcode.com/problems/missing-number/

Tier 1 — must prepare · Math & Bit Manipulation

The array holds n distinct values from the range [0, n]. Return the missing one.

There is a sum formula answer and an XOR answer. The XOR one does not overflow.

Example:
    Input:  nums = [3, 0, 1]
    Output: 2

Run: python math_bits/tier1/missing_number.py
"""


def missing_number(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert missing_number([3, 0, 1]) == 2
    assert missing_number([0, 1]) == 2
    assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    print("ok")
