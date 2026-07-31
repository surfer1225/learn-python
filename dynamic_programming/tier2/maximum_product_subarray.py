"""Maximum Product Subarray
https://leetcode.com/problems/maximum-product-subarray/

Tier 2 — good to prepare · Dynamic Programming

Return the largest product of any contiguous subarray.

Unlike max-sum, negatives flip the ordering — so track the running minimum too.

Example:
    Input:  nums = [2, 3, -2, 4]
    Output: 6

Run: python dynamic_programming/tier2/maximum_product_subarray.py
"""


def max_product(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_product([2, 3, -2, 4]) == 6
    assert max_product([-2, 0, -1]) == 0
    assert max_product([-2, 3, -4]) == 24
    print("ok")
