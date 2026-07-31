"""Edit Distance
https://leetcode.com/problems/edit-distance/

Tier 3 — prepare if you have time · Dynamic Programming

Return the minimum number of insertions, deletions, or substitutions needed to
turn `word1` into `word2` (Levenshtein distance).

Example:
    Input:  word1 = "horse", word2 = "ros"
    Output: 3

Run: python dynamic_programming/tier3/edit_distance.py
"""


def min_distance(word1: str, word2: str) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_distance("horse", "ros") == 3
    assert min_distance("intention", "execution") == 5
    assert min_distance("", "abc") == 3
    print("ok")
