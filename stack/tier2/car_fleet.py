"""Car Fleet
https://leetcode.com/problems/car-fleet/

Tier 2 — good to prepare · Stack

Cars head toward a target at `position[i]` with speed `speed[i]`. A faster car
catching a slower one joins its fleet and travels at the slower speed. Return
the number of fleets that arrive.

Process cars from closest-to-target backwards and compare arrival times.

Example:
    Input:  target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]
    Output: 3

Run: python stack/tier2/car_fleet.py
"""


def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert car_fleet(10, [3], [3]) == 1
    assert car_fleet(100, [0, 2, 4], [4, 2, 1]) == 1
    print("ok")
