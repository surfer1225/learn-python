"""Task Scheduler
https://leetcode.com/problems/task-scheduler/

Tier 2 — good to prepare · Heap / Priority Queue

Identical tasks must be separated by at least `n` intervals; the CPU may idle.
Return the minimum number of intervals to finish all tasks.

There is a greedy heap solution and a closed-form counting one. Know both.

Example:
    Input:  tasks = ["A", "A", "A", "B", "B", "B"], n = 2
    Output: 8        # A B idle A B idle A B

Run: python heap/tier2/task_scheduler.py
"""


def least_interval(tasks: list[str], n: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert least_interval(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert least_interval(["A", "A", "A", "B", "B", "B"], 0) == 6
    assert least_interval(["A", "C", "A", "B", "D", "B"], 1) == 6
    print("ok")
