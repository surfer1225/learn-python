"""Maximum Subarray
https://leetcode.com/problems/maximum-subarray/

Tier 1 — must prepare · Greedy

Return the largest sum of any contiguous subarray (Kadane's algorithm).

Be able to state the one-line invariant: at each index, either extend the
previous subarray or start fresh.

Example:
    Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    Output: 6        # [4, -1, 2, 1]

Run: python greedy/tier1/maximum_subarray.py
"""


def max_sub_array(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_sub_array([1]) == 1
    assert max_sub_array([5, 4, -1, 7, 8]) == 23
    assert max_sub_array([-3, -1, -2]) == -1
    print("ok")
