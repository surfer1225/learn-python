"""Daily Temperatures
https://leetcode.com/problems/daily-temperatures/

Tier 1 — must prepare · Stack

For each day, how many days until a warmer temperature? Put 0 where no warmer
day exists.

The canonical monotonic-stack problem — recognise the shape and the rest follow.

Example:
    Input:  temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    Output: [1, 1, 4, 2, 1, 1, 0, 0]

Run: python stack/tier1/daily_temperatures.py
"""


def daily_temperatures(temperatures: list[int]) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
    print("ok")
