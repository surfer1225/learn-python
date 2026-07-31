"""Jump Game II
https://leetcode.com/problems/jump-game-ii/

Tier 2 — good to prepare · Greedy

Return the minimum number of jumps to reach the last index. Reaching it is
guaranteed.

Think of it as BFS over levels, done with two pointers instead of a queue.

Example:
    Input:  nums = [2, 3, 1, 1, 4]
    Output: 2

Run: python greedy/tier2/jump_game_ii.py
"""


def jump(nums: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert jump([2, 3, 1, 1, 4]) == 2
    assert jump([2, 3, 0, 1, 4]) == 2
    assert jump([0]) == 0
    print("ok")
