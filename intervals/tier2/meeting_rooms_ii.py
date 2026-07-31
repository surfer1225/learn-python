"""Meeting Rooms II
https://leetcode.com/problems/meeting-rooms-ii/

Tier 2 — good to prepare · Intervals

Return the minimum number of conference rooms required.

Two standard framings: a min-heap of end times, or sorting starts and ends
separately and sweeping. The sweep generalises to many scheduling problems.

Example:
    Input:  [[0, 30], [5, 10], [15, 20]]
    Output: 2

Run: python intervals/tier2/meeting_rooms_ii.py
"""


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
    assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
    assert min_meeting_rooms([]) == 0
    print("ok")
