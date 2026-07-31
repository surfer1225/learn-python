"""Longest String Chain
https://leetcode.com/problems/longest-string-chain/

Tier 3 — prepare if you have time · Arrays & Hashing

`word_a` is a predecessor of `word_b` if inserting exactly one letter into
`word_a` makes it equal `word_b`. Return the length of the longest possible
chain of words from `words`.

Example:
    Input:  words = ["a", "b", "ba", "bca", "bda", "bdca"]
    Output: 4        # a -> ba -> bda -> bdca

Run: python arrays/tier3/longest_string_chain.py
"""


def longest_str_chain(words: list[str]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert longest_str_chain(["a", "b", "ba", "bca", "bda", "bdca"]) == 4
    assert longest_str_chain(["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]) == 5
    assert longest_str_chain(["abcd", "dbqca"]) == 1
    print("ok")
