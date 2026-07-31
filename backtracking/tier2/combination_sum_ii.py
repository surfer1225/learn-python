"""Combination Sum II
https://leetcode.com/problems/combination-sum-ii/

Tier 2 — good to prepare · Backtracking

Each candidate may be used at most once, and the result must contain no
duplicate combinations. Candidates may repeat in the input.

Example:
    Input:  candidates = [10, 1, 2, 7, 6, 1, 5], target = 8
    Output: [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]

Run: python backtracking/tier2/combination_sum_ii.py
"""


def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(c) for c in combination_sum2([10, 1, 2, 7, 6, 1, 5], 8)) == [
        [1, 1, 6], [1, 2, 5], [1, 7], [2, 6],
    ]
    assert sorted(sorted(c) for c in combination_sum2([2, 5, 2, 1, 2], 5)) == [[1, 2, 2], [5]]
    print("ok")
