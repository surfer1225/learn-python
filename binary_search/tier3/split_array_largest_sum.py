"""Split Array Largest Sum
https://leetcode.com/problems/split-array-largest-sum/

Tier 3 — prepare if you have time · Binary Search

Split `nums` into `k` non-empty contiguous subarrays so the largest subarray sum
is as small as possible. Return that sum.

Another binary-search-on-the-answer, with a greedy feasibility check.

Example:
    Input:  nums = [7, 2, 5, 10, 8], k = 2
    Output: 18

Run: python binary_search/tier3/split_array_largest_sum.py
"""


def split_array(nums: list[int], k: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert split_array([7, 2, 5, 10, 8], 2) == 18
    assert split_array([1, 2, 3, 4, 5], 2) == 9
    assert split_array([1, 4, 4], 3) == 4
    print("ok")
