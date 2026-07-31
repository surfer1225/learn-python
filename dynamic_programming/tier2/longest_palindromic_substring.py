"""Longest Palindromic Substring
https://leetcode.com/problems/longest-palindromic-substring/

Tier 2 — good to prepare · Dynamic Programming

Return the longest palindromic substring of `s`.

Expand-around-centre is O(n^2) time and O(1) space, and is easier to get right
under pressure than the 2D DP table.

Example:
    Input:  s = "babad"
    Output: "bab"    # "aba" is equally valid

Run: python dynamic_programming/tier2/longest_palindromic_substring.py
"""


def longest_palindrome(s: str) -> str:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("a") == "a"
    print("ok")
