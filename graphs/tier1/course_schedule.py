"""Course Schedule
https://leetcode.com/problems/course-schedule/

Tier 1 — must prepare · Graphs

`prerequisites[i] = [a, b]` means you must take b before a. Return whether all
courses can be finished — i.e. whether the directed graph is acyclic.

Example:
    Input:  num_courses = 2, prerequisites = [[1, 0], [0, 1]]
    Output: False

Run: python graphs/tier1/course_schedule.py
"""


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(5, []) is True
    print("ok")
