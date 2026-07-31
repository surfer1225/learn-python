"""Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/

Tier 1 — must prepare · Arrays & Hashing

Given an integer array `nums` and an integer `k`, return the `k` most frequent
elements. The answer is guaranteed to be unique; return it in any order.

Follow-up: can you do better than O(n log n)?

Example:
    Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
    Output: [1, 2]

Run: python arrays/tier1/top_k_frequent_elements.py
"""


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert top_k_frequent([1], 1) == [1]
    assert sorted(top_k_frequent([4, 4, 4, 5, 5, 6], 3)) == [4, 5, 6]
    print("ok")
