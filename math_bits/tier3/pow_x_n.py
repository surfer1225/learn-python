"""Pow(x, n)
https://leetcode.com/problems/powx-n/

Tier 3 — prepare if you have time · Math & Bit Manipulation

Implement pow(x, n) — x raised to the power n — in O(log n) via fast
exponentiation. Handle negative exponents.

Example:
    Input:  x = 2.0, n = 10
    Output: 1024.0

Run: python math_bits/tier3/pow_x_n.py
"""


def my_pow(x: float, n: int) -> float:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert my_pow(2.0, 10) == 1024.0
    assert my_pow(2.0, -2) == 0.25
    assert my_pow(2.0, 0) == 1.0
    assert abs(my_pow(2.1, 3) - 9.261) < 1e-9
    print("ok")
