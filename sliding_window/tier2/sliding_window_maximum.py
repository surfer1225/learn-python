"""Sliding Window Maximum
https://leetcode.com/problems/sliding-window-maximum/

Tier 2 — good to prepare · Sliding Window

Return the maximum of every contiguous window of size `k`.

O(n) is expected: keep a monotonically decreasing deque of indices.

Example:
    Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    Output: [3, 3, 5, 5, 6, 7]

Run: python sliding_window/tier2/sliding_window_maximum.py
"""


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    assert max_sliding_window([1, -1], 1) == [1, -1]
    print("ok")
