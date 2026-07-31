"""Word Break
https://leetcode.com/problems/word-break/

Tier 1 — must prepare · Dynamic Programming

Return whether `s` can be segmented into a space-separated sequence of one or
more dictionary words. Words may be reused.

Example:
    Input:  s = "leetcode", word_dict = ["leet", "code"]
    Output: True

Run: python dynamic_programming/tier1/word_break.py
"""


def word_break(s: str, word_dict: list[str]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print("ok")
