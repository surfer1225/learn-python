"""Non-overlapping Intervals
https://leetcode.com/problems/non-overlapping-intervals/

Tier 1 — must prepare · Intervals

Return the minimum number of intervals to remove so the rest do not overlap.

Greedy: sort by end time and keep the interval that finishes earliest. Be ready
to argue why sorting by start is worse.

Example:
    Input:  [[1, 2], [2, 3], [3, 4], [1, 3]]
    Output: 1

Run: python intervals/tier1/non_overlapping_intervals.py
"""


def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
    assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
    assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
    print("ok")
