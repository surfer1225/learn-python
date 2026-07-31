"""Happy Number
https://leetcode.com/problems/happy-number/

Tier 3 — prepare if you have time · Math & Bit Manipulation

Repeatedly replace the number with the sum of the squares of its digits. It is
happy if this reaches 1; otherwise it loops forever. Return whether n is happy.

Cycle detection again — a set works, but Floyd's algorithm uses O(1) space.

Example:
    Input:  n = 19
    Output: True     # 1+81=82, 64+4=68, 36+64=100, 1

Run: python math_bits/tier3/happy_number.py
"""


def is_happy(n: int) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_happy(19) is True
    assert is_happy(2) is False
    assert is_happy(1) is True
    print("ok")
