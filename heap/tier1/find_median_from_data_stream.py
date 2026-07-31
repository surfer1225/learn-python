"""Find Median from Data Stream
https://leetcode.com/problems/find-median-from-data-stream/

Tier 1 — must prepare · Heap / Priority Queue

Support `add_num` and `find_median` over a growing stream.

Two heaps — a max-heap for the lower half, a min-heap for the upper — keep the
median at the boundary. Python only has a min-heap; negate to fake the other.

Example:
    Input:  add(1), add(2), find_median(), add(3), find_median()
    Output: 1.5, then 2.0

Run: python heap/tier1/find_median_from_data_stream.py
"""


class MedianFinder:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def add_num(self, num: int) -> None:
        raise NotImplementedError

    def find_median(self) -> float:
        raise NotImplementedError


if __name__ == "__main__":
    finder = MedianFinder()
    finder.add_num(1)
    finder.add_num(2)
    assert finder.find_median() == 1.5
    finder.add_num(3)
    assert finder.find_median() == 2.0
    print("ok")
