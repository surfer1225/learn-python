"""Course Schedule II
https://leetcode.com/problems/course-schedule-ii/

Tier 2 — good to prepare · Graphs

Return any valid order in which to take all courses, or [] if impossible.
This is a topological sort — know both Kahn's algorithm and the DFS version.

Example:
    Input:  num_courses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output: [0, 1, 2, 3] or [0, 2, 1, 3]

Run: python graphs/tier2/course_schedule_ii.py
"""


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    edges = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = find_order(4, edges)
    position = {course: i for i, course in enumerate(order)}
    assert sorted(order) == [0, 1, 2, 3]
    assert all(position[pre] < position[course] for course, pre in edges)
    assert find_order(2, [[1, 0], [0, 1]]) == []
    assert find_order(1, []) == [0]
    print("ok")
