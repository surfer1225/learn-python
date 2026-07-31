"""Valid Palindrome
https://leetcode.com/problems/valid-palindrome/

Tier 1 — must prepare · Two Pointers

Return `True` if `s` is a palindrome after lowercasing and removing every
non-alphanumeric character.

Example:
    Input:  s = "A man, a plan, a canal: Panama"
    Output: True

Run: python two_pointers/tier1/valid_palindrome.py
"""


def is_palindrome(s: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("race a car") is False
    assert is_palindrome(" ") is True
    print("ok")
