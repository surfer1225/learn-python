"""Cheapest Flights Within K Stops
https://leetcode.com/problems/cheapest-flights-within-k-stops/

Tier 3 — prepare if you have time · Graphs

Find the cheapest price from `src` to `dst` using at most `k` stops, or -1.

Plain Dijkstra breaks here — the stop limit means a cheaper path may be
unusable. Bellman-Ford over k + 1 relaxation rounds is the clean answer.

Example:
    Input:  n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]],
            src = 0, dst = 3, k = 1
    Output: 700

Run: python graphs/tier3/cheapest_flights_within_k_stops.py
"""


def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    flights = [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]]
    assert find_cheapest_price(4, flights, 0, 3, 1) == 700
    assert find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert find_cheapest_price(3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
    print("ok")
