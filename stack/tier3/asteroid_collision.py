"""Asteroid Collision
https://leetcode.com/problems/asteroid-collision/

Tier 3 — prepare if you have time · Stack

Positive values move right, negative move left, all at the same speed. When two
collide the smaller explodes; equal sizes destroy both. Return the final state.

Example:
    Input:  asteroids = [5, 10, -5]
    Output: [5, 10]

Run: python stack/tier3/asteroid_collision.py
"""


def asteroid_collision(asteroids: list[int]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert asteroid_collision([5, 10, -5]) == [5, 10]
    assert asteroid_collision([8, -8]) == []
    assert asteroid_collision([10, 2, -5]) == [10]
    assert asteroid_collision([-2, -1, 1, 2]) == [-2, -1, 1, 2]
    print("ok")
