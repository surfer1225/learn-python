"""Merge Intervals
https://leetcode.com/problems/merge-intervals/

Tier 1 — must prepare · Intervals

Merge all overlapping intervals and return the non-overlapping intervals that
cover the same span.

Example:
    Input:  [[1, 3], [2, 6], [8, 10], [15, 18]]
    Output: [[1, 6], [8, 10], [15, 18]]

Run: python intervals/tier1/merge_intervals.py
"""


def merge(intervals: list[list[int]]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge([[1, 4]]) == [[1, 4]]
    print("ok")
