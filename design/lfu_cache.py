"""LFU (Least Frequently Used) cache — O(1) get and put.

https://leetcode.com/problems/lfu-cache/

Eviction rule (LeetCode 460): when full, remove the least-FREQUENTLY used key;
if several keys tie on frequency, remove the least-RECENTLY used among them.

The design is "LRU, but bucketed by frequency":

    _key_map:  key  -> _Node(value, freq)          # O(1) lookup
    _freq_map: freq -> OrderedDict[key -> _Node]    # per-frequency LRU buckets
    _min_freq: the smallest non-empty frequency     # O(1) eviction target

Each bucket is an OrderedDict so it doubles as an LRU list *within* one
frequency: leftmost = least-recently-used, rightmost = most-recent. `_min_freq`
means eviction never has to scan for the minimum frequency.

(For a pure hand-rolled version, swap each OrderedDict for a dict + doubly
linked list — the same DLL used in lru_cache.py. OrderedDict already *is* a
dict + DLL internally, so it keeps the code short while staying O(1).)
"""

from __future__ import annotations

from collections import OrderedDict, defaultdict


class _Node:
    __slots__ = ("key", "value", "freq")

    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.freq = 1


class LFUCache:
    """Fixed-capacity LFU cache with O(1) get and put (LeetCode 460)."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._key_map: dict[int, _Node] = {}
        # defaultdict so an empty bucket is created on demand.
        self._freq_map: dict[int, "OrderedDict[int, _Node]"] = defaultdict(OrderedDict)
        self._min_freq = 0

    # -- internal: bump a node's frequency by one --------------------------
    def _bump(self, node: _Node) -> None:
        """Move `node` from its current frequency bucket to freq+1. O(1)."""
        f = node.freq
        bucket = self._freq_map[f]
        del bucket[node.key]                 # leave the old bucket

        # If we just emptied the current minimum bucket, the new minimum is f+1.
        if f == self._min_freq and not bucket:
            del self._freq_map[f]            # keep the map tidy
            self._min_freq += 1

        node.freq = f + 1
        self._freq_map[node.freq][node.key] = node   # join the higher bucket (as MRU)

    # -- public API --------------------------------------------------------
    def get(self, key: int) -> int:
        """Return the value and increment the key's frequency, else -1."""
        node = self._key_map.get(key)
        if node is None:
            return -1
        self._bump(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert/update `key`; evict the LFU (LRU-tiebreak) entry if full."""
        if self.capacity <= 0:
            return

        node = self._key_map.get(key)
        if node is not None:                 # existing key: update + bump freq
            node.value = value
            self._bump(node)
            return

        if len(self._key_map) >= self.capacity:   # full: evict before inserting
            lfu_bucket = self._freq_map[self._min_freq]
            evict_key, _ = lfu_bucket.popitem(last=False)   # LRU within min freq
            if not lfu_bucket:
                del self._freq_map[self._min_freq]
            del self._key_map[evict_key]

        node = _Node(key, value)             # fresh key always starts at freq 1
        self._key_map[key] = node
        self._freq_map[1][key] = node
        self._min_freq = 1                   # a brand-new key is the least frequent

    def __len__(self) -> int:
        return len(self._key_map)

    def __repr__(self) -> str:
        parts = []
        for f in sorted(self._freq_map):
            keys = list(self._freq_map[f].keys())
            if keys:
                parts.append(f"f{f}:{keys}")
        return f"LFUCache(cap={self.capacity}, min_freq={self._min_freq}, {' '.join(parts)})"


# ===========================================================================
# Self-checks
# ===========================================================================
def _test_leetcode() -> None:
    # The canonical LeetCode 460 example.
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1        # freq: 1->2
    c.put(3, 3)                 # cache full; keys 1(f2) and 2(f1) -> evict 2 (LFU)
    assert c.get(2) == -1       # 2 was evicted
    assert c.get(3) == 3        # freq: 3 -> 2
    c.put(4, 4)                 # tie at f2 between 1 and 3 -> evict 1 (LRU of the tie)
    assert c.get(1) == -1       # 1 was evicted
    assert c.get(3) == 3
    assert c.get(4) == 4
    print("ok  LeetCode 460")


def _test_frequency_tiebreak() -> None:
    # When frequencies tie, the LEAST-RECENTLY-USED key is evicted.
    c = LFUCache(3)
    c.put(1, 10)
    c.put(2, 20)
    c.put(3, 30)               # all at freq 1: order [1, 2, 3]
    c.get(1)                   # 1 -> freq 2
    c.get(2)                   # 2 -> freq 2 ; freq-1 bucket now just [3]
    c.put(4, 40)               # full: min_freq=1, only key 3 there -> evict 3
    assert c.get(3) == -1
    # Remaining: 1(f2), 2(f2), 4(f1). Insert 5 -> evict 4 (only key at min freq 1).
    c.put(5, 50)
    assert c.get(4) == -1
    assert c.get(1) == 10 and c.get(2) == 20 and c.get(5) == 50
    print("ok  frequency + LRU tie-break")


def _test_update_counts_as_use() -> None:
    # put() on an existing key bumps its frequency (it's a use).
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 100)              # key 1: freq 1 -> 2 (and value updated)
    c.put(3, 3)               # evicts key 2 (freq 1, the LFU), not key 1
    assert c.get(2) == -1
    assert c.get(1) == 100
    print("ok  update counts as a use")


def _test_zero_capacity() -> None:
    c = LFUCache(0)
    c.put(1, 1)               # no-op
    assert c.get(1) == -1
    assert len(c) == 0
    print("ok  capacity == 0 edge case")


if __name__ == "__main__":
    _test_leetcode()
    _test_frequency_tiebreak()
    _test_update_counts_as_use()
    _test_zero_capacity()
    print("all LFU tests passed")
