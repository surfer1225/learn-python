"""Counting Bits
https://leetcode.com/problems/counting-bits/

Tier 1 — must prepare · Math & Bit Manipulation

Return an array where `ans[i]` is the number of set bits in `i`, for 0 <= i <= n.

O(n) total is expected — reuse previously computed answers rather than counting
each number independently.

Example:
    Input:  n = 5
    Output: [0, 1, 1, 2, 1, 2]

Run: python math_bits/tier1/counting_bits.py
"""


def count_bits(n: int) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert count_bits(2) == [0, 1, 1]
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert count_bits(0) == [0]
    print("ok")
