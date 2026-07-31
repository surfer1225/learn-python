"""4Sum
https://leetcode.com/problems/4sum/

Tier 3 — prepare if you have time · Two Pointers

Return all unique quadruplets summing to `target`. Generalise your 3Sum
approach rather than writing a fourth nested loop.

Example:
    Input:  nums = [1, 0, -1, 0, -2, 2], target = 0
    Output: [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]

Run: python two_pointers/tier3/four_sum.py
"""


def four_sum(nums: list[int], target: int) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(q) for q in four_sum([1, 0, -1, 0, -2, 2], 0)) == [
        [-2, -1, 1, 2],
        [-2, 0, 0, 2],
        [-1, 0, 0, 1],
    ]
    assert sorted(sorted(q) for q in four_sum([2, 2, 2, 2, 2], 8)) == [[2, 2, 2, 2]]
    print("ok")
