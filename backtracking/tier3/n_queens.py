"""N-Queens
https://leetcode.com/problems/n-queens/

Tier 3 — prepare if you have time · Backtracking

Place `n` queens on an n x n board so none attack each other. Return every
distinct solution as a list of board rows ('Q' and '.').

The interesting part is the O(1) attack check — three sets, not a board scan.

Example:
    Input:  n = 4
    Output: [[".Q..","...Q","Q...","..Q."], ["..Q.","Q...","...Q",".Q.."]]

Run: python backtracking/tier3/n_queens.py
"""


def solve_n_queens(n: int) -> list[list[str]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(solve_n_queens(4)) == sorted(
        [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
    )
    assert solve_n_queens(1) == [["Q"]]
    assert solve_n_queens(3) == []
    print("ok")
