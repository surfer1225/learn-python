"""Largest Rectangle in Histogram
https://leetcode.com/problems/largest-rectangle-in-histogram/

Tier 2 — good to prepare · Stack

Each bar has width 1 and height `heights[i]`. Return the area of the largest
rectangle contained in the histogram.

O(n) with a monotonic increasing stack. Hard, but it unlocks several others.

Example:
    Input:  heights = [2, 1, 5, 6, 2, 3]
    Output: 10

Run: python stack/tier2/largest_rectangle_in_histogram.py
"""


def largest_rectangle_area(heights: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle_area([2, 4]) == 4
    assert largest_rectangle_area([]) == 0
    print("ok")
