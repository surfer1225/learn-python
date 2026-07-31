"""Last Stone Weight
https://leetcode.com/problems/last-stone-weight/

Tier 2 — good to prepare · Heap / Priority Queue

Repeatedly smash the two heaviest stones together: equal weights destroy both,
otherwise the heavier is replaced by the difference. Return the last stone's
weight, or 0 if none remain.

Example:
    Input:  stones = [2, 7, 4, 1, 8, 1]
    Output: 1

Run: python heap/tier2/last_stone_weight.py
"""


def last_stone_weight(stones: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert last_stone_weight([2, 7, 4, 1, 8, 1]) == 1
    assert last_stone_weight([1]) == 1
    assert last_stone_weight([2, 2]) == 0
    print("ok")
