"""Sliding Window Maximum
https://leetcode.com/problems/sliding-window-maximum/

Given an array `nums` and window size `k`, return the max of each sliding window.
"""

from typing import List


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    print("ok")
