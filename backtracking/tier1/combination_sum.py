"""Combination Sum
https://leetcode.com/problems/combination-sum/

Tier 1 — must prepare · Backtracking

Return all unique combinations of `candidates` (distinct values) summing to
`target`. The same number may be reused unlimited times.

Example:
    Input:  candidates = [2, 3, 6, 7], target = 7
    Output: [[2, 2, 3], [7]]

Run: python backtracking/tier1/combination_sum.py
"""


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(c) for c in combination_sum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
    assert sorted(sorted(c) for c in combination_sum([2, 3, 5], 8)) == [
        [2, 2, 2, 2], [2, 3, 3], [3, 5],
    ]
    assert combination_sum([2], 1) == []
    print("ok")
