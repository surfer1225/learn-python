"""Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Tier 1 — must prepare · Sliding Window

Return the length of the longest substring of `s` with no repeated characters.

Example:
    Input:  s = "abcabcbb"
    Output: 3        # "abc"

Run: python sliding_window/tier1/longest_substring_without_repeating_characters.py
"""


def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}  # char -> most recent index seen
    start = 0  # left edge of the current window
    best = 0

    for i, ch in enumerate(s):
        # Only jump `start` forward if the duplicate is inside the window;
        # a stale index from before `start` must be ignored (see "abba").
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)

    return best


if __name__ == "__main__":
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("abba") == 2  # stale-index trap
    assert length_of_longest_substring("dvdf") == 3  # stale-index trap
    assert length_of_longest_substring("a") == 1
    assert length_of_longest_substring("au") == 2
    assert length_of_longest_substring("tmmzuxt") == 5  # "mzuxt"
    assert length_of_longest_substring(" ") == 1
    print("ok")
