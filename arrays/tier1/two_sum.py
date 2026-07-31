"""Two Sum
https://leetcode.com/problems/two-sum/

Tier 1 — must prepare · Arrays & Hashing

Given an array of integers `nums` and an integer `target`, return the indices of
the two numbers that add up to `target`.

Example:
    Input:  nums = [2, 7, 11, 15], target = 9
    Output: [0, 1]

Run: python arrays/tier1/two_sum.py
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    """Return the indices of the one pair summing to `target`.

    Time: O(n) — a single pass with O(1) average dict operations.
    Space: O(n) — the seen map holds up to n entries.
    """
    seen: dict[int, int] = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # LeetCode guarantees exactly one solution; unreachable


if __name__ == "__main__":
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]
    assert sorted(two_sum([3, 2, 4], 6)) == [1, 2]
    assert sorted(two_sum([3, 3], 6)) == [0, 1]
    print("ok")
