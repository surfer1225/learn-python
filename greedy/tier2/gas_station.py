"""Gas Station
https://leetcode.com/problems/gas-station/

Tier 2 — good to prepare · Greedy

Return the starting station index from which you can complete the circuit once,
or -1. The answer is unique when it exists.

Two facts do all the work: if total gas >= total cost a solution exists, and if
you run dry at station i, no station between the start and i can work either.

Example:
    Input:  gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2]
    Output: 3

Run: python greedy/tier2/gas_station.py
"""


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete_circuit([2, 3, 4], [3, 4, 3]) == -1
    assert can_complete_circuit([5], [4]) == 0
    print("ok")
