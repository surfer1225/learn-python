"""Maximum Swap
https://leetcode.com/problems/maximum-swap/

Tier 2 — good to prepare · Greedy

Given a non-negative integer `num`, you may swap two of its digits at most
once. Return the maximum value you can get. 0 <= num <= 10^8.

Example:
    Input:  num = 2736
    Output: 7236     # swap the 2 and the 7

Run: python greedy/tier2/maximum_swap.py
"""


def maximum_swap(num: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert maximum_swap(2736) == 7236
    assert maximum_swap(9973) == 9973  # already maximal: no swap
    assert maximum_swap(1993) == 9913  # tie: take the LAST 9
    assert maximum_swap(98368) == 98863  # first digits already in place
    assert maximum_swap(115) == 511
    assert maximum_swap(10) == 10
    assert maximum_swap(0) == 0
    print("ok")
