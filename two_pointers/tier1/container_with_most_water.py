"""Container With Most Water
https://leetcode.com/problems/container-with-most-water/

Tier 1 — must prepare · Two Pointers

Each element is a vertical line's height. Pick two lines that, with the x-axis,
hold the most water. Return that maximum area.

Be ready to justify why moving the taller pointer can never help.

Example:
    Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    Output: 49

Run: python two_pointers/tier1/container_with_most_water.py
"""


def max_area(height: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    print("ok")
