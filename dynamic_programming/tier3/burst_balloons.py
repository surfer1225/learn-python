"""Burst Balloons
https://leetcode.com/problems/burst-balloons/

Tier 3 — prepare if you have time · Dynamic Programming

Bursting balloon i earns nums[i-1] * nums[i] * nums[i+1] coins, with out-of-range
values treated as 1. Return the maximum coins obtainable.

Interval DP. The insight is to iterate over the balloon burst *last* in each
interval, not first.

Example:
    Input:  nums = [3, 1, 5, 8]
    Output: 167

Run: python dynamic_programming/tier3/burst_balloons.py
"""


def max_coins(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_coins([3, 1, 5, 8]) == 167
    assert max_coins([1, 5]) == 10
    assert max_coins([]) == 0
    print("ok")
