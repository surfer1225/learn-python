"""Permutation in String
https://leetcode.com/problems/permutation-in-string/

Tier 2 — good to prepare · Sliding Window

Return `True` if `s2` contains a permutation of `s1` as a substring.

A fixed-size window plus a character count comparison beats re-sorting.

Example:
    Input:  s1 = "ab", s2 = "eidbaooo"
    Output: True

Run: python sliding_window/tier2/permutation_in_string.py
"""


def check_inclusion(s1: str, s2: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert check_inclusion("ab", "eidbaooo") is True
    assert check_inclusion("ab", "eidboaoo") is False
    assert check_inclusion("adc", "dcda") is True
    print("ok")
