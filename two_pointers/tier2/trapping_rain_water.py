"""Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/

Tier 2 — good to prepare · Two Pointers

Given an elevation map, compute how much rain water it can trap.

There are three standard solutions: extra arrays, a monotonic stack, and two
pointers with O(1) space. Know at least two.

Example:
    Input:  height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    Output: 6

Run: python two_pointers/tier2/trapping_rain_water.py
"""


def trap(height: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9
    assert trap([]) == 0
    print("ok")
