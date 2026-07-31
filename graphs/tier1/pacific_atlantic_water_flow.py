"""Pacific Atlantic Water Flow
https://leetcode.com/problems/pacific-atlantic-water-flow/

Tier 1 — must prepare · Graphs

Water flows from a cell to neighbours of equal or lower height. The Pacific
touches the top and left edges, the Atlantic the bottom and right. Return all
cells from which water can reach both oceans.

Searching from every cell is wasteful — search *inward* from each ocean instead.

Example:
    Input:  a 5x5 height grid (see the test below)
    Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]

Run: python graphs/tier1/pacific_atlantic_water_flow.py
"""


def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    heights = [
        [1, 2, 2, 3, 5],
        [3, 2, 3, 4, 4],
        [2, 4, 5, 3, 1],
        [6, 7, 1, 4, 5],
        [5, 1, 1, 2, 4],
    ]
    assert sorted(pacific_atlantic(heights)) == [
        [0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0],
    ]
    assert pacific_atlantic([[1]]) == [[0, 0]]
    print("ok")
