"""Substring with Concatenation of All Words
https://leetcode.com/problems/substring-with-concatenation-of-all-words/

Tier 3 — prepare if you have time · Sliding Window

All words in `words` have the same length. Return every starting index in `s`
of a substring that is a concatenation of each word exactly once, in any order.

Example:
    Input:  s = "barfoothefoobarman", words = ["foo", "bar"]
    Output: [0, 9]

Run: python sliding_window/tier3/substring_with_concatenation_of_all_words.py
"""


def find_substring(s: str, words: list[str]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(find_substring("barfoothefoobarman", ["foo", "bar"])) == [0, 9]
    assert find_substring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []
    assert sorted(find_substring("barfoofoobarthefoobarman", ["bar", "foo", "the"])) == [6, 9, 12]
    print("ok")
