"""Jump Game
https://leetcode.com/problems/jump-game/

Tier 1 — must prepare · Greedy

Each element is the maximum jump length from that position. Return whether you
can reach the last index.

Track the furthest reachable index in one pass — no DP needed.

Example:
    Input:  nums = [3, 2, 1, 0, 4]
    Output: False

Run: python greedy/tier1/jump_game.py
"""


def can_jump(nums: list[int]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_jump([2, 3, 1, 1, 4]) is True
    assert can_jump([3, 2, 1, 0, 4]) is False
    assert can_jump([0]) is True
    print("ok")
