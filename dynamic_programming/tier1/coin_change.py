"""Coin Change
https://leetcode.com/problems/coin-change/

Tier 1 — must prepare · Dynamic Programming

Return the fewest coins needed to make `amount`, or -1 if impossible. You have
an unlimited supply of each denomination.

Greedy fails here — be ready with a counterexample.

Example:
    Input:  coins = [1, 2, 5], amount = 11
    Output: 3        # 5 + 5 + 1

Run: python dynamic_programming/tier1/coin_change.py
"""


def coin_change(coins: list[int], amount: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    print("ok")
