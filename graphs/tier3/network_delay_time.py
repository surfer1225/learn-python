"""Network Delay Time
https://leetcode.com/problems/network-delay-time/

Tier 3 — prepare if you have time · Graphs

`times[i] = [u, v, w]` is a directed edge with travel time w. Return how long
until all `n` nodes receive a signal sent from `k`, or -1 if some cannot.

Dijkstra with a heap.

Example:
    Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
    Output: 2

Run: python graphs/tier3/network_delay_time.py
"""


def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert network_delay_time([[1, 2, 1]], 2, 1) == 1
    assert network_delay_time([[1, 2, 1]], 2, 2) == -1
    print("ok")
