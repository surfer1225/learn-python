"""Insert Interval
https://leetcode.com/problems/insert-interval/

Tier 1 — must prepare · Intervals

Insert `new_interval` into a list of non-overlapping intervals sorted by start,
merging where necessary. Keep the result sorted and non-overlapping.

Doable in O(n) without re-sorting — three phases: before, overlapping, after.

Example:
    Input:  intervals = [[1, 3], [6, 9]], new_interval = [2, 5]
    Output: [[1, 5], [6, 9]]

Run: python intervals/tier1/insert_interval.py
"""


def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2], [3, 10], [12, 16],
    ]
    assert insert([], [5, 7]) == [[5, 7]]
    print("ok")
