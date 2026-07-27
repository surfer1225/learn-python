"""Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array `nums` and an integer `k`, return the `k` most frequent
elements.
"""

from typing import List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    print("ok")
