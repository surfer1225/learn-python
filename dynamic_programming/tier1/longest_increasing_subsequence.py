"""Longest Increasing Subsequence
https://leetcode.com/problems/longest-increasing-subsequence/

Tier 1 — must prepare · Dynamic Programming

Return the length of the longest strictly increasing subsequence.

O(n^2) DP is the expected first answer; the O(n log n) patience-sorting version
with `bisect` is the follow-up.

Example:
    Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
    Output: 4        # [2, 3, 7, 101]

Run: python dynamic_programming/tier1/longest_increasing_subsequence.py
"""


def length_of_lis(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7]) == 1
    assert length_of_lis([]) == 0
    print("ok")
