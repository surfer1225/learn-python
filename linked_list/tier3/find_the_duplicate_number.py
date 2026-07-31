"""Find the Duplicate Number
https://leetcode.com/problems/find-the-duplicate-number/

Tier 3 — prepare if you have time · Linked List

`nums` holds n + 1 integers in the range [1, n], so at least one value repeats.
Return it without modifying the array and using O(1) extra space.

The array is a linked list in disguise: i -> nums[i]. Now it is cycle detection.

Example:
    Input:  nums = [1, 3, 4, 2, 2]
    Output: 2

Run: python linked_list/tier3/find_the_duplicate_number.py
"""


def find_duplicate(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert find_duplicate([1, 3, 4, 2, 2]) == 2
    assert find_duplicate([3, 1, 3, 4, 2]) == 3
    assert find_duplicate([1, 1]) == 1
    print("ok")
