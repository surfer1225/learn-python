"""Longest Repeating Character Replacement
https://leetcode.com/problems/longest-repeating-character-replacement/

Tier 1 — must prepare · Sliding Window

You may change at most `k` characters of `s` to any uppercase letter. Return the
length of the longest substring of a single repeated letter you can produce.

A window is valid when (window length - count of its most frequent letter) <= k.

Example:
    Input:  s = "AABABBA", k = 1
    Output: 4

Run: python sliding_window/tier1/longest_repeating_character_replacement.py
"""


def character_replacement(s: str, k: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert character_replacement("ABAB", 2) == 4
    assert character_replacement("AABABBA", 1) == 4
    assert character_replacement("", 0) == 0
    print("ok")
