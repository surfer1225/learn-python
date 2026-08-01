"""Kth Largest Element in an Array
https://leetcode.com/problems/kth-largest-element-in-an-array/

Tier 1 — must prepare · Heap / Priority Queue

Return the kth largest element (by sorted order, not distinctness).

Sorting is O(n log n); a size-k heap is O(n log k); quickselect averages O(n).
Be ready to compare all three.

Example:
    Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
    Output: 5

Run: python heap/tier1/kth_largest_element_in_an_array.py
"""

import heapq
from typing import Any, Protocol, TypeVar


class Comparable(Protocol):
    """Anything with a total order: int, str, float, date, Decimal, ...

    A heap needs exactly one capability — `<` — so that is all we require.
    `typing` ships no such protocol, and `other: Any` with a positional-only
    `/` is what makes built-ins like `int.__lt__(self, value: int)` match.
    """

    def __lt__(self, other: Any, /) -> bool: ...


C = TypeVar("C", bound=Comparable)


def find_kth_largest(nums: list[C], k: int) -> C:
    """Return the kth largest element (by sorted order, not distinctness).

    Generic over any orderable type, not just `int`. Does not modify `nums`.

    Time: O(n log k) — `nlargest` keeps a bounded heap of size k.
    Space: O(k).

    Raises:
        ValueError: if k is outside 1..len(nums), which would otherwise fail
            as a bare IndexError from the `[-1]`.
    """
    if not 1 <= k <= len(nums):
        raise ValueError(f"k must be in 1..{len(nums)}, got {k}")
    # nlargest returns descending, so the last of the k largest IS the kth.
    return heapq.nlargest(k, nums)[-1]


if __name__ == "__main__":
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    assert find_kth_largest([1], 1) == 1

    # generic: any orderable type, not just int
    assert find_kth_largest(["pear", "apple", "fig"], 2) == "fig"
    assert find_kth_largest([1.5, 0.5, 2.5], 1) == 2.5

    # the input must come back untouched
    original = [3, 2, 1, 5, 6, 4]
    find_kth_largest(original, 2)
    assert original == [3, 2, 1, 5, 6, 4], original

    # out-of-range k is a clear error, not an IndexError
    for bad_nums, bad_k in (([], 1), ([1, 2], 0), ([1, 2], 3)):
        try:
            find_kth_largest(bad_nums, bad_k)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad_nums}, k={bad_k}")

    print("ok")
