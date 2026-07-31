"""Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Tier 1 — must prepare · Stack

Given a string of '()[]{}', determine if the brackets are closed in the correct
order and every opener has a matching closer.

Example:
    Input:  s = "()[]{}"
    Output: True

Run: python stack/tier1/valid_parentheses.py
"""


def is_valid(s: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("([)]") is False
    assert is_valid("{[]}") is True
    assert is_valid("") is True
    print("ok")
