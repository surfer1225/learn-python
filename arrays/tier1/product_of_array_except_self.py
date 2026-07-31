"""Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Tier 1 — must prepare · Arrays & Hashing

Return an array `answer` such that `answer[i]` is the product of all elements of
`nums` except `nums[i]`. Do it without division and in O(n).

Example:
    Input:  nums = [1, 2, 3, 4]
    Output: [24, 12, 8, 6]

Run: python arrays/tier1/product_of_array_except_self.py
"""


def product_except_self(nums: list[int]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    print("ok")
