"""Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers `nums` and an integer `target`, return the indices of
the two numbers that add up to `target`.
"""

from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in map:
            return [map[complement], i]
        map[num] = i
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]
    print("ok")
