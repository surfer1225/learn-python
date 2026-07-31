"""Generate Parentheses
https://leetcode.com/problems/generate-parentheses/

Tier 2 — good to prepare · Stack

Given `n` pairs of parentheses, generate all combinations of well-formed
parentheses.

Example:
    Input:  n = 3
    Output: ["((()))", "(()())", "(())()", "()(())", "()()()"]

Run: python stack/tier2/generate_parentheses.py
"""


def generate_parenthesis(n: int) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(generate_parenthesis(3)) == sorted(
        ["((()))", "(()())", "(())()", "()(())", "()()()"]
    )
    assert generate_parenthesis(1) == ["()"]
    print("ok")
