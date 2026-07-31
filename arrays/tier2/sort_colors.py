"""Sort Colors
https://leetcode.com/problems/sort-colors/

Tier 2 — good to prepare · Arrays & Hashing

Sort an array of 0s, 1s, and 2s in place so equal values are adjacent, in the
order 0, 1, 2. Use only constant extra space and a single pass (Dutch national
flag).

Example:
    Input:  nums = [2, 0, 2, 1, 1, 0]
    Output: [0, 0, 1, 1, 2, 2]

Run: python arrays/tier2/sort_colors.py
"""


def sort_colors(nums: list[int]) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    nums = [2, 0, 2, 1, 1, 0]
    sort_colors(nums)
    assert nums == [0, 0, 1, 1, 2, 2]
    nums = [2, 0, 1]
    sort_colors(nums)
    assert nums == [0, 1, 2]
    print("ok")
