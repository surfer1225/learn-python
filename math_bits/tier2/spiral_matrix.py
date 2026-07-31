"""Spiral Matrix
https://leetcode.com/problems/spiral-matrix/

Tier 2 — good to prepare · Math & Bit Manipulation

Return all elements of an m x n matrix in spiral order.

Pure boundary bookkeeping — the difficulty is writing it without an off-by-one.

Example:
    Input:  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

Run: python math_bits/tier2/spiral_matrix.py
"""


def spiral_order(matrix: list[list[int]]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [
        1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7,
    ]
    assert spiral_order([]) == []
    print("ok")
