"""LRU (Least Recently Used) cache — full implementations.

https://leetcode.com/problems/lru-cache/

This module contains two classes:

    LRUCache      -- the exact LeetCode-146 interface (get/put, O(1), -1 on miss).
                     Hand-rolled hash map + doubly linked list, no library help,
                     which is what interviewers want to see.

    LRUCacheProd  -- an industry-style cache built on the SAME core, adding the
                     features real caches need: generic keys/values, per-entry
                     TTL, get_or_load (compute-on-miss), peek, invalidate,
                     hit/miss/eviction stats, and thread-safety.

Why a dict + doubly linked list?
    * dict:  key -> node        -> O(1) lookup ("where is this key's node?")
    * DLL:   recency order      -> O(1) move-to-front / evict-from-back
Neither alone gives both fast lookup AND fast recency updates; together they do.
Sentinel (dummy) head/tail nodes remove all the empty/first/last edge cases, so
every insert and unlink is the same handful of pointer writes.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Generic, Hashable, Optional, TypeVar


# ===========================================================================
# 1. LeetCode 146 — the interview solution
# ===========================================================================
class _Node:
    """A doubly linked list node holding one cache entry."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    """Fixed-capacity LRU cache with O(1) get and put (LeetCode 146)."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._map: dict[int, _Node] = {}

        # Sentinels: real nodes always live strictly between head and tail.
        # head <-> (MRU) <-> ... <-> (LRU) <-> tail
        self._head = _Node()
        self._tail = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

    # -- O(1) linked-list primitives ---------------------------------------
    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _Node) -> None:
        first = self._head.next
        node.prev, node.next = self._head, first
        self._head.next = node
        first.prev = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._add_front(node)

    # -- public API --------------------------------------------------------
    def get(self, key: int) -> int:
        """Return the value for `key` and mark it most-recently-used, else -1."""
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update `key`; evict the least-recently-used entry if full."""
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        node = _Node(key, value)
        self._map[key] = node
        self._add_front(node)

        if len(self._map) > self.capacity:
            lru = self._tail.prev        # the node just before the tail sentinel
            self._remove(lru)
            del self._map[lru.key]

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:
        # MRU -> LRU order, useful for debugging.
        items, cur = [], self._head.next
        while cur is not self._tail:
            items.append(f"{cur.key}:{cur.value}")
            cur = cur.next
        return f"LRUCache(cap={self.capacity}, [{' -> '.join(items)}])"


# ===========================================================================
# 2. Production-style LRU cache — same core, real-world surface
# ===========================================================================
K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_MISS = object()  # unique sentinel so `None` is a valid cached value


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


@dataclass
class _Entry(Generic[K, V]):
    key: K
    value: V
    expires_at: Optional[float] = None  # monotonic deadline; None = never
    prev: Optional["_Entry[K, V]"] = field(default=None, repr=False)
    next: Optional["_Entry[K, V]"] = field(default=None, repr=False)


class LRUCacheProd(Generic[K, V]):
    """Thread-safe LRU cache with TTL, compute-on-miss, peek, and stats.

    Design mirrors Guava/Caffeine/cachetools: the LRU core is identical to
    `LRUCache` above; everything else is a thin layer on top.
    """

    def __init__(self, capacity: int, *, default_ttl: Optional[float] = None,
                 time_fn: Callable[[], float] = time.monotonic):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.default_ttl = default_ttl
        self._now = time_fn
        self._map: dict[K, _Entry[K, V]] = {}
        self._lock = threading.RLock()
        self.stats = CacheStats()

        self._head: _Entry = _Entry(None, None)  # sentinels
        self._tail: _Entry = _Entry(None, None)
        self._head.next = self._tail
        self._tail.prev = self._head

    # -- list primitives (O(1)) --------------------------------------------
    def _remove(self, e: _Entry) -> None:
        e.prev.next = e.next
        e.next.prev = e.prev

    def _add_front(self, e: _Entry) -> None:
        first = self._head.next
        e.prev, e.next = self._head, first
        self._head.next = e
        first.prev = e

    def _touch(self, e: _Entry) -> None:
        self._remove(e)
        self._add_front(e)

    def _is_expired(self, e: _Entry) -> bool:
        return e.expires_at is not None and self._now() >= e.expires_at

    def _evict_entry(self, e: _Entry, *, expired: bool) -> None:
        self._remove(e)
        del self._map[e.key]
        if expired:
            self.stats.expirations += 1
        else:
            self.stats.evictions += 1

    # -- public API --------------------------------------------------------
    def get(self, key: K, default: V | None = None) -> V | None:
        """Return the value (marking it MRU), or `default` on miss/expiry."""
        with self._lock:
            e = self._map.get(key)
            if e is None:
                self.stats.misses += 1
                return default
            if self._is_expired(e):
                self._evict_entry(e, expired=True)
                self.stats.misses += 1
                return default
            self._touch(e)
            self.stats.hits += 1
            return e.value

    def put(self, key: K, value: V, *, ttl: Optional[float] = _MISS) -> None:  # type: ignore[assignment]
        """Insert/update `key`. `ttl` seconds overrides default_ttl (None = never)."""
        with self._lock:
            effective_ttl = self.default_ttl if ttl is _MISS else ttl
            expires_at = self._now() + effective_ttl if effective_ttl is not None else None

            e = self._map.get(key)
            if e is not None:
                e.value = value
                e.expires_at = expires_at
                self._touch(e)
                return

            e = _Entry(key, value, expires_at)
            self._map[key] = e
            self._add_front(e)
            if len(self._map) > self.capacity:
                self._evict_entry(self._tail.prev, expired=False)

    def get_or_load(self, key: K, loader: Callable[[K], V], *,
                    ttl: Optional[float] = _MISS) -> V:  # type: ignore[assignment]
        """Return cached value, or compute it via `loader(key)`, store, and return.

        This is the single most important production method: it turns the
        cache-miss-then-recompute race into one call. (For brevity the loader
        runs under the lock; a real system would load per-key to avoid blocking
        unrelated keys.)
        """
        with self._lock:
            sentinel_default = _MISS
            existing = self.get(key, default=sentinel_default)  # type: ignore[arg-type]
            if existing is not sentinel_default:
                return existing  # type: ignore[return-value]
            value = loader(key)
            self.put(key, value, ttl=ttl)
            return value

    def contains(self, key: K) -> bool:
        """Membership WITHOUT counting as a use (a peek). Respects expiry."""
        with self._lock:
            e = self._map.get(key)
            if e is None:
                return False
            if self._is_expired(e):
                self._evict_entry(e, expired=True)
                return False
            return True

    def invalidate(self, key: K) -> bool:
        """Remove `key`. Returns True if it was present."""
        with self._lock:
            e = self._map.get(key)
            if e is None:
                return False
            self._remove(e)
            del self._map[key]
            return True

    def clear(self) -> None:
        with self._lock:
            self._map.clear()
            self._head.next = self._tail
            self._tail.prev = self._head

    def __len__(self) -> int:
        with self._lock:
            return len(self._map)

    def __contains__(self, key: K) -> bool:
        return self.contains(key)


# ===========================================================================
# Self-checks
# ===========================================================================
def _test_leetcode() -> None:
    # The canonical LeetCode 146 example.
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1          # returns 1; 1 is now MRU
    c.put(3, 3)                   # evicts key 2
    assert c.get(2) == -1         # not found
    c.put(4, 4)                   # evicts key 1
    assert c.get(1) == -1         # not found
    assert c.get(3) == 3
    assert c.get(4) == 4

    # Updating an existing key counts as a use.
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)                  # update + promote 1
    c.put(3, 3)                   # evicts 2 (the LRU), not 1
    assert c.get(2) == -1
    assert c.get(1) == 10
    print("ok  LeetCode 146")


def _test_prod() -> None:
    c: LRUCacheProd[str, int] = LRUCacheProd(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)                 # evicts "b"
    assert c.get("b") is None
    assert c.get("b", default=-1) == -1
    assert "a" in c and "b" not in c
    assert c.stats.evictions == 1

    # get_or_load computes on miss exactly once, then caches.
    calls = []
    c.clear()
    c.stats = CacheStats()
    load = lambda k: (calls.append(k), len(k))[1]
    assert c.get_or_load("xy", load) == 2   # miss -> loads
    assert c.get_or_load("xy", load) == 2   # hit  -> no reload
    assert calls == ["xy"]

    # TTL expiry using a controllable clock.
    clock = {"t": 1000.0}
    t = LRUCacheProd[str, int](10, default_ttl=5, time_fn=lambda: clock["t"])
    t.put("k", 42)
    assert t.get("k") == 42
    clock["t"] += 6                          # advance past the 5s TTL
    assert t.get("k") is None                # expired
    assert t.stats.expirations == 1
    print("ok  LRUCacheProd (TTL, get_or_load, peek, stats)")


def _test_thread_safety() -> None:
    import concurrent.futures as cf

    c: LRUCacheProd[int, int] = LRUCacheProd(128)

    def worker(n: int) -> None:
        for i in range(1000):
            c.put((n * 1000 + i) % 200, i)
            c.get(i % 200)

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(worker, range(8)))
    # No exception + size stays within capacity = the lock held under contention.
    assert len(c) <= 128
    print("ok  thread-safety (8 threads, no corruption)")


if __name__ == "__main__":
    _test_leetcode()
    _test_prod()
    _test_thread_safety()
    print("all LRU tests passed")
