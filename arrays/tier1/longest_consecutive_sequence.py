"""Longest Consecutive Sequence
https://leetcode.com/problems/longest-consecutive-sequence/

Tier 1 — must prepare · Arrays & Hashing

Given an unsorted array of integers, return the length of the longest sequence
of consecutive elements. Must run in O(n) — so sorting is off the table.

Example:
    Input:  nums = [100, 4, 200, 1, 3, 2]
    Output: 4        # the sequence 1, 2, 3, 4

Run: python arrays/tier1/longest_consecutive_sequence.py
"""


def longest_consecutive(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    print("ok")
