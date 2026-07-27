"""Course Schedule
https://leetcode.com/problems/course-schedule/

Given `numCourses` and a list of prerequisite pairs, return True if you can
finish all courses (i.e. the dependency graph has no cycle).
"""

from typing import List


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    print("ok")
