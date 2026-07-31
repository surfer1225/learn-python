"""Reverse Bits
https://leetcode.com/problems/reverse-bits/

Tier 1 — must prepare · Math & Bit Manipulation

Reverse the bits of a 32-bit unsigned integer.

Python ints are arbitrary precision, so you must be explicit about the 32-bit
width — that detail is the point of the question here.

Example:
    Input:  n = 43261596
    Output: 964176192

Run: python math_bits/tier1/reverse_bits.py
"""


def reverse_bits(n: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert reverse_bits(43261596) == 964176192
    assert reverse_bits(0) == 0
    assert reverse_bits(1) == 2147483648
    print("ok")
