"""Set Matrix Zeroes
https://leetcode.com/problems/set-matrix-zeroes/

Tier 2 — good to prepare · Math & Bit Manipulation

If a cell is 0, set its entire row and column to 0, in place.

The O(1)-space version uses the first row and column as the marker storage —
watch the ordering carefully.

Example:
    Input:  [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    Output: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

Run: python math_bits/tier2/set_matrix_zeroes.py
"""


def set_zeroes(matrix: list[list[int]]) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    set_zeroes(matrix)
    assert matrix == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
    matrix = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    set_zeroes(matrix)
    assert matrix == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
    print("ok")
