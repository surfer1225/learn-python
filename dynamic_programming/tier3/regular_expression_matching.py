"""Regular Expression Matching
https://leetcode.com/problems/regular-expression-matching/

Tier 3 — prepare if you have time · Dynamic Programming

Implement matching for '.' (any single character) and '*' (zero or more of the
preceding element). The match must cover the entire input string.

Example:
    Input:  s = "aab", p = "c*a*b"
    Output: True

Run: python dynamic_programming/tier3/regular_expression_matching.py
"""


def is_match(s: str, p: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_match("aa", "a") is False
    assert is_match("aa", "a*") is True
    assert is_match("ab", ".*") is True
    assert is_match("aab", "c*a*b") is True
    assert is_match("mississippi", "mis*is*p*.") is False
    print("ok")
