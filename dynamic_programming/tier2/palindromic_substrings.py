"""Palindromic Substrings
https://leetcode.com/problems/palindromic-substrings/

Tier 2 — good to prepare · Dynamic Programming

Count how many palindromic substrings `s` contains. Substrings at different
positions count separately even if identical.

Example:
    Input:  s = "aaa"
    Output: 6        # "a" x3, "aa" x2, "aaa"

Run: python dynamic_programming/tier2/palindromic_substrings.py
"""


def count_substrings(s: str) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert count_substrings("abc") == 3
    assert count_substrings("aaa") == 6
    assert count_substrings("") == 0
    print("ok")
