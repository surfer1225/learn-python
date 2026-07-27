"""Number of Islands
https://leetcode.com/problems/number-of-islands/

Given an m x n 2D grid of '1' (land) and '0' (water), return the number of
islands.
"""

from typing import List


def num_islands(grid: List[List[str]]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert num_islands(grid) == 3
    print("ok")
