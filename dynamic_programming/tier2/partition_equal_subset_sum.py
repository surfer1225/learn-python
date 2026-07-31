"""Partition Equal Subset Sum
https://leetcode.com/problems/partition-equal-subset-sum/

Tier 2 — good to prepare · Dynamic Programming

Return whether the array can be split into two subsets with equal sums.

This is 0/1 knapsack in disguise: can any subset reach total / 2?

Example:
    Input:  nums = [1, 5, 11, 5]
    Output: True     # [1, 5, 5] and [11]

Run: python dynamic_programming/tier2/partition_equal_subset_sum.py
"""


def can_partition(nums: list[int]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
    assert can_partition([1, 1]) is True
    print("ok")
