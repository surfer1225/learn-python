"""Rotate Image
https://leetcode.com/problems/rotate-image/

Tier 2 — good to prepare · Math & Bit Manipulation

Rotate an n x n matrix 90 degrees clockwise, in place.

Transpose then reverse each row — know why that composition works.

Example:
    Input:  [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

Run: python math_bits/tier2/rotate_image.py
"""


def rotate(matrix: list[list[int]]) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    rotate(matrix)
    assert matrix == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    matrix = [[1]]
    rotate(matrix)
    assert matrix == [[1]]
    print("ok")
