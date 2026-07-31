"""Subarray Sum Equals K
https://leetcode.com/problems/subarray-sum-equals-k/

Tier 2 — good to prepare · Arrays & Hashing

Return the total number of contiguous subarrays whose sum equals `k`.
Values may be negative, which rules out a sliding window.

Example:
    Input:  nums = [1, 1, 1], k = 2
    Output: 2

Run: python arrays/tier2/subarray_sum_equals_k.py
"""


def subarray_sum(nums: list[int], k: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum([1, -1, 0], 0) == 3
    print("ok")
