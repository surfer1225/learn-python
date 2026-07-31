"""Number of 1 Bits
https://leetcode.com/problems/number-of-1-bits/

Tier 1 — must prepare · Math & Bit Manipulation

Return the number of set bits in an unsigned integer (its Hamming weight).

Know the `n & (n - 1)` trick and what it does.

Example:
    Input:  n = 11        # 0b1011
    Output: 3

Run: python math_bits/tier1/number_of_1_bits.py
"""


def hamming_weight(n: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert hamming_weight(11) == 3
    assert hamming_weight(128) == 1
    assert hamming_weight(0) == 0
    assert hamming_weight(2147483645) == 30
    print("ok")
