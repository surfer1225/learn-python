"""Meeting Rooms
https://leetcode.com/problems/meeting-rooms/

Tier 2 — good to prepare · Intervals

Given meeting time intervals, determine whether one person could attend all of
them.

Example:
    Input:  [[0, 30], [5, 10], [15, 20]]
    Output: False

Run: python intervals/tier2/meeting_rooms.py
"""


def can_attend_meetings(intervals: list[list[int]]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
    assert can_attend_meetings([[7, 10], [2, 4]]) is True
    assert can_attend_meetings([]) is True
    print("ok")
