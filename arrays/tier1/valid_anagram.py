"""Valid Anagram
https://leetcode.com/problems/valid-anagram/

Tier 1 — must prepare · Arrays & Hashing

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`.

Example:
    Input:  s = "anagram", t = "nagaram"
    Output: True

Run: python arrays/tier1/valid_anagram.py
"""


def is_anagram(s: str, t: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_anagram("anagram", "nagaram") is True
    assert is_anagram("rat", "car") is False
    assert is_anagram("", "") is True
    assert is_anagram("a", "ab") is False
    print("ok")
