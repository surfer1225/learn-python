"""Climbing Stairs
https://leetcode.com/problems/climbing-stairs/

Tier 1 — must prepare · Dynamic Programming

You climb 1 or 2 steps at a time. In how many distinct ways can you reach the
top of `n` steps?

The simplest DP there is — and the one to use for practising the O(1)-space
rolling-variable rewrite.

Example:
    Input:  n = 3
    Output: 3        # 1+1+1, 1+2, 2+1

Run: python dynamic_programming/tier1/climbing_stairs.py
"""


def climb_stairs(n: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    assert climb_stairs(1) == 1
    print("ok")
