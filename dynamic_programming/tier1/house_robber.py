"""House Robber
https://leetcode.com/problems/house-robber/

Tier 1 — must prepare · Dynamic Programming

You cannot rob two adjacent houses. Return the maximum you can take.

Example:
    Input:  nums = [2, 7, 9, 3, 1]
    Output: 12       # 2 + 9 + 1

Run: python dynamic_programming/tier1/house_robber.py
"""


def rob(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([]) == 0
    assert rob([5]) == 5
    print("ok")
