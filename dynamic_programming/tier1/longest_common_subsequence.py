"""Longest Common Subsequence
https://leetcode.com/problems/longest-common-subsequence/

Tier 1 — must prepare · Dynamic Programming

Return the length of the longest subsequence common to both strings.

The canonical 2D grid DP. Get comfortable drawing the table and reading the
recurrence off it.

Example:
    Input:  text1 = "abcde", text2 = "ace"
    Output: 3        # "ace"

Run: python dynamic_programming/tier1/longest_common_subsequence.py
"""


def longest_common_subsequence(text1: str, text2: str) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    print("ok")
