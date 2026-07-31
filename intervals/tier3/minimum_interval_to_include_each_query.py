"""Minimum Interval to Include Each Query
https://leetcode.com/problems/minimum-interval-to-include-each-query/

Tier 3 — prepare if you have time · Intervals

For each query, return the size of the smallest interval containing it, or -1.
Interval [l, r] has size r - l + 1.

Sort queries and intervals, then sweep with a heap — offline processing.

Example:
    Input:  intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2, 3, 4, 5]
    Output: [3, 3, 1, 4]

Run: python intervals/tier3/minimum_interval_to_include_each_query.py
"""


def min_interval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert min_interval([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]) == [3, 3, 1, 4]
    assert min_interval([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]) == [2, -1, 4, 6]
    print("ok")
