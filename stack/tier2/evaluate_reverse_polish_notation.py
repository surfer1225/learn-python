"""Evaluate Reverse Polish Notation
https://leetcode.com/problems/evaluate-reverse-polish-notation/

Tier 2 — good to prepare · Stack

Evaluate an arithmetic expression in Reverse Polish Notation. Division between
two integers truncates toward zero — note that Python's `//` does not.

Example:
    Input:  tokens = ["2", "1", "+", "3", "*"]
    Output: 9        # (2 + 1) * 3

Run: python stack/tier2/evaluate_reverse_polish_notation.py
"""


def eval_rpn(tokens: list[str]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
    print("ok")
