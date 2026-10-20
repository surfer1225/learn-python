"""Valid Anagram
https://leetcode.com/problems/valid-anagram/

Tier 1 — must prepare · Arrays & Hashing

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`.

Example:
    Input:  s = "anagram", t = "nagaram"
    Output: True

Run: python arrays/tier1/valid_anagram.py
"""
from collections import Counter

def is_anagram(s: str, t: str) -> bool:
    s_char_dict = dict(Counter(s))
    t_char_dict = dict(Counter(t))
    return s_char_dict == t_char_dict


if __name__ == "__main__":
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("", "") is True
    assert is_anagram("a", "ab") is False
    print("ok")
