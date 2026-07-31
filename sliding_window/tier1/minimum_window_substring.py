"""Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Tier 1 — must prepare · Sliding Window

Return the shortest substring of `s` containing every character of `t`
(including duplicates). Return "" if none exists.

Example:
    Input:  s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"

Run: python sliding_window/tier1/minimum_window_substring.py
"""


def min_window(s: str, t: str) -> str:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
    print("ok")
