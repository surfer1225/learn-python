"""Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Tier 1 — must prepare · Sliding Window

Return the length of the longest substring of `s` with no repeated characters.

Example:
    Input:  s = "abcabcbb"
    Output: 3        # "abc"

Run: python sliding_window/tier1/longest_substring_without_repeating_characters.py
"""


def length_of_longest_substring(s: str) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    print("ok")
