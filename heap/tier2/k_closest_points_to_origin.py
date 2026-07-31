"""K Closest Points to Origin
https://leetcode.com/problems/k-closest-points-to-origin/

Tier 2 — good to prepare · Heap / Priority Queue

Return the `k` points closest to the origin, in any order.

Note that you never need the square root — say why.

Example:
    Input:  points = [[3, 3], [5, -1], [-2, 4]], k = 2
    Output: [[3, 3], [-2, 4]]

Run: python heap/tier2/k_closest_points_to_origin.py
"""


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert k_closest([[1, 3], [-2, 2]], 1) == [[-2, 2]]
    assert sorted(k_closest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]
    print("ok")
