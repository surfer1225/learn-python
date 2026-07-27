"""Minimum Window Substring
https://leetcode.com/problems/minimum-window-substring/

Given strings `s` and `t`, return the minimum window substring of `s` that
contains all characters of `t`. Return "" if no such window exists.
"""


def min_window(s: str, t: str) -> str:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "aa") == ""
    print("ok")
