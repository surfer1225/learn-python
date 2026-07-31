"""House Robber II
https://leetcode.com/problems/house-robber-ii/

Tier 2 — good to prepare · Dynamic Programming

Same as House Robber, but the houses are in a circle — the first and last are
adjacent.

Reduce it to the linear version rather than writing new DP.

Example:
    Input:  nums = [2, 3, 2]
    Output: 3

Run: python dynamic_programming/tier2/house_robber_ii.py
"""


def rob(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert rob([2, 3, 2]) == 3
    assert rob([1, 2, 3, 1]) == 4
    assert rob([1]) == 1
    assert rob([1, 2]) == 2
    print("ok")
