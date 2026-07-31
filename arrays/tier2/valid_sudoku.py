"""Valid Sudoku
https://leetcode.com/problems/valid-sudoku/

Tier 2 — good to prepare · Arrays & Hashing

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be
validated: each row, column, and 3x3 sub-box must contain no repeated digit.
Empty cells are '.' and the board does not have to be solvable.

Example:
    Input:  a board whose first row is ["5","3",".",".","7",".",".",".","."]
    Output: True

Run: python arrays/tier2/valid_sudoku.py
"""


def is_valid_sudoku(board: list[list[str]]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    assert is_valid_sudoku(board) is True
    board[0][0] = "8"  # collides with the 8 in the same column
    assert is_valid_sudoku(board) is False
    print("ok")
