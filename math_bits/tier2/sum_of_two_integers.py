"""Sum of Two Integers
https://leetcode.com/problems/sum-of-two-integers/

Tier 2 — good to prepare · Math & Bit Manipulation

Return a + b without using + or -.

XOR gives the sum without carry, AND-shift gives the carry. In Python you must
also handle the lack of fixed-width overflow explicitly.

Example:
    Input:  a = 2, b = 3
    Output: 5

Run: python math_bits/tier2/sum_of_two_integers.py
"""


def get_sum(a: int, b: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert get_sum(1, 2) == 3
    assert get_sum(2, 3) == 5
    assert get_sum(-1, 1) == 0
    assert get_sum(-2, -3) == -5
    print("ok")
