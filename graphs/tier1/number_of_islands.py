"""Number of Islands
https://leetcode.com/problems/number-of-islands/

Tier 1 — must prepare · Graphs

Count the islands in a grid of '1' (land) and '0' (water). An island is land
connected horizontally or vertically and surrounded by water.

Example:
    Input:  [["1","1","0"],["1","0","0"],["0","0","1"]]
    Output: 2

Run: python graphs/tier1/number_of_islands.py
"""


def num_islands(grid: list[list[str]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert num_islands([
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]) == 1
    assert num_islands([
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]) == 3
    assert num_islands([]) == 0
    print("ok")
