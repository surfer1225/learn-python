"""Alien Dictionary
https://leetcode.com/problems/alien-dictionary/

Tier 3 — prepare if you have time · Graphs

Given words sorted lexicographically in an unknown alphabet, derive an ordering
of its letters. Return "" if no valid order exists.

Build edges from the first differing character of adjacent words, then topo sort.
The invalid-prefix case is the edge case people miss.

Example:
    Input:  words = ["wrt", "wrf", "er", "ett", "rftt"]
    Output: "wertf"

Run: python graphs/tier3/alien_dictionary.py
"""


def alien_order(words: list[str]) -> str:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""
    print("ok")
