"""3Sum
https://leetcode.com/problems/3sum/

Tier 1 — must prepare · Two Pointers

Return all unique triplets `[nums[i], nums[j], nums[k]]` that sum to zero.
The solution set must not contain duplicate triplets — handling that cleanly is
the real difficulty.

Example:
    Input:  nums = [-1, 0, 1, 2, -1, -4]
    Output: [[-1, -1, 2], [-1, 0, 1]]

Run: python two_pointers/tier1/three_sum.py
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(sorted(t) for t in three_sum([-1, 0, 1, 2, -1, -4])) == [
        [-1, -1, 2],
        [-1, 0, 1],
    ]
    assert three_sum([0, 1, 1]) == []
    assert sorted(sorted(t) for t in three_sum([0, 0, 0, 0])) == [[0, 0, 0]]
    print("ok")
