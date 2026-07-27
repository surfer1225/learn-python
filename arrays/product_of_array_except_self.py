"""Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/

Return an array `answer` such that `answer[i]` is the product of all elements of
`nums` except `nums[i]`. Do it without division and in O(n).
"""

from typing import List


def product_except_self(nums: List[int]) -> List[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    print("ok")
