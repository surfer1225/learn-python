"""Move Zeroes
https://leetcode.com/problems/move-zeroes/

Tier 2 — good to prepare · Two Pointers

Move all 0s to the end of `nums` in place while keeping the relative order of
the non-zero elements. Minimise the number of writes.

Example:
    Input:  nums = [0, 1, 0, 3, 12]
    Output: [1, 3, 12, 0, 0]

Run: python two_pointers/tier2/move_zeroes.py
"""


def move_zeroes(nums: list[int]) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    nums = [0, 1, 0, 3, 12]
    move_zeroes(nums)
    assert nums == [1, 3, 12, 0, 0]
    nums = [0]
    move_zeroes(nums)
    assert nums == [0]
    print("ok")
