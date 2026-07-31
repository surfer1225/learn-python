"""Search a 2D Matrix
https://leetcode.com/problems/search-a-2d-matrix/

Tier 2 — good to prepare · Binary Search

Each row is sorted, and the first value of each row exceeds the last of the
previous row. Return whether `target` is present, in O(log(m*n)).

Example:
    Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
    Output: True

Run: python binary_search/tier2/search_a_2d_matrix.py
"""


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    assert search_matrix(matrix, 3) is True
    assert search_matrix(matrix, 13) is False
    assert search_matrix([[1]], 1) is True
    print("ok")
