"""Surrounded Regions
https://leetcode.com/problems/surrounded-regions/

Tier 2 — good to prepare · Graphs

Flip every 'O' region fully surrounded by 'X' to 'X'. Regions touching the
border survive. Modify the board in place.

Invert the problem: find what is *reachable from the border* and protect it.

Example:
    Input:  [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

Run: python graphs/tier2/surrounded_regions.py
"""


def solve(board: list[list[str]]) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    board = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"],
    ]
    solve(board)
    assert board == [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"],
    ]
    print("ok")
