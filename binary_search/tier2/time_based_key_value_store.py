"""Time Based Key-Value Store
https://leetcode.com/problems/time-based-key-value-store/

Tier 2 — good to prepare · Binary Search

Store multiple timestamped values per key. `get(key, timestamp)` returns the
value with the largest stored timestamp <= the requested one, or "".
Timestamps are strictly increasing per key.

Example:
    Input:  set("foo", "bar", 1), get("foo", 1), get("foo", 3)
    Output: "bar", "bar"

Run: python binary_search/tier2/time_based_key_value_store.py
"""


class TimeMap:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def set(self, key: str, value: str, timestamp: int) -> None:
        raise NotImplementedError

    def get(self, key: str, timestamp: int) -> str:
        raise NotImplementedError


if __name__ == "__main__":
    store = TimeMap()
    store.set("foo", "bar", 1)
    assert store.get("foo", 1) == "bar"
    assert store.get("foo", 3) == "bar"
    store.set("foo", "bar2", 4)
    assert store.get("foo", 4) == "bar2"
    assert store.get("foo", 5) == "bar2"
    assert store.get("foo", 0) == ""
    assert store.get("nope", 1) == ""
    print("ok")
