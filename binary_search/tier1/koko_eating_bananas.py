"""Koko Eating Bananas
https://leetcode.com/problems/koko-eating-bananas/

Tier 1 — must prepare · Binary Search

Koko eats `k` bananas per hour from one pile at a time. Return the smallest `k`
letting her finish all piles within `h` hours.

This is binary search on the *answer*, not on the array — learn to spot it.

Example:
    Input:  piles = [3, 6, 7, 11], h = 8
    Output: 4

Run: python binary_search/tier1/koko_eating_bananas.py
"""


def min_eating_speed(piles: list[int], h: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    print("ok")
