"""Visual aid for the LRU (Least Recently Used) cache algorithm.

Run it:
    python experiments/lru_cache_visualization.py

The window shows the TWO data structures an LRU cache is built from, side by side:

    * HASH MAP  (left)  : key -> node reference.  Gives O(1) lookup.
    * DOUBLY LINKED LIST (right): recency order. Front = most-recently-used (MRU),
                                  back = least-recently-used (LRU). Gives O(1) reorder.

Neither structure alone is enough: the map finds a node instantly but knows
nothing about recency; the list tracks recency but can't find a key without a
scan. Together every operation is O(1):

    get(key) : map lookup -> if hit, move node to front. O(1)
    put(k,v) : insert/update at front; if over capacity, evict the tail. O(1)

Type a key/value and press Put or Get, or press "Run Demo" for a scripted trace.
When the cache is full, a Put of a NEW key evicts the LRU node (back of the list),
and its entry is removed from the map too — watch both panels update.
"""

from __future__ import annotations

import tkinter as tk

# --- layout -----------------------------------------------------------------
CANVAS_W, CANVAS_H = 1180, 560
MAP_X = 40                 # left edge of the hash-map panel
MAP_W = 220
MAP_TOP = 110
MAP_ROW_H = 46

DLL_LEFT = 360            # HEAD sentinel x
ROW_Y = 300
NODE_W, NODE_H = 104, 66
STEP = 132
MAX_CAP = 6

# --- colors -----------------------------------------------------------------
NODE_FILL = "#dbeafe"
NODE_EDGE = "#1d4ed8"
SENTINEL_FILL = "#e5e7eb"
SENTINEL_EDGE = "#6b7280"
HOT_HIT = "#fde68a"        # accessed / updated
HOT_NEW = "#bbf7d0"        # freshly inserted
HOT_EVICT = "#fecaca"      # about to be evicted
NEXT_COLOR = "#1d4ed8"
PREV_COLOR = "#b45309"
LINK_COLOR = "#9333ea"     # map -> node connector for the active key

ANIM_FRAMES = 20
ANIM_INTERVAL_MS = 16
DEMO_PAUSE_MS = 800


class Node:
    def __init__(self, key: int, value: int, label: str | None = None):
        self.key = key
        self.value = value
        self.sentinel_label = label
        self.prev: Node | None = None
        self.next: Node | None = None
        # view state
        self.x = DLL_LEFT
        self.y = ROW_Y
        self.tx = DLL_LEFT
        self.ty = ROW_Y

    @property
    def is_sentinel(self) -> bool:
        return self.sentinel_label is not None

    @property
    def text(self) -> str:
        return self.sentinel_label if self.is_sentinel else f"{self.key}:{self.value}"


class LRUCache:
    """LRU cache. Each op returns an 'event' dict describing what changed so the
    visualizer can animate it. This is the real LeetCode-146 logic."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: dict[int, Node] = {}
        self.head = Node(0, 0, label="HEAD (MRU)")
        self.tail = Node(0, 0, label="TAIL (LRU)")
        self.head.next = self.tail
        self.tail.prev = self.head

    # -- O(1) list primitives ----------------------------------------------
    def _insert_front(self, node: Node) -> None:
        first = self.head.next
        node.prev, node.next = self.head, first
        self.head.next = node
        first.prev = node

    def _unlink(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node: Node) -> None:
        self._unlink(node)
        self._insert_front(node)

    # -- public API ---------------------------------------------------------
    def get(self, key: int) -> dict:
        if key not in self.map:
            return {"type": "get_miss", "key": key}
        node = self.map[key]
        self._move_to_front(node)
        return {"type": "get_hit", "key": key, "node": node, "value": node.value}

    def put(self, key: int, value: int) -> dict:
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._move_to_front(node)
            return {"type": "put_update", "key": key, "node": node}

        node = Node(key, value)
        self._insert_front(node)
        self.map[key] = node
        evicted = None
        if len(self.map) > self.capacity:
            evicted = self.tail.prev
            self._unlink(evicted)
            del self.map[evicted.key]
        return {"type": "put_insert", "key": key, "node": node, "evicted": evicted}

    def real_nodes(self) -> list[Node]:
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur)
            cur = cur.next
        return out


def _ease_out(t: float) -> float:
    return 1 - (1 - t) ** 3


class LRUVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("LRU Cache — visual aid")
        root.resizable(False, False)

        self.capacity = 3
        self.cache = LRUCache(self.capacity)
        self.leaving: list[Node] = []          # evicted nodes sliding out
        self.highlight: dict[Node, str] = {}   # node -> fill color this op
        self.active_key: int | None = None     # draws map->node connector
        self.animating = False
        self.pending: list[tuple] = []         # queued operations (clicks + demo)
        self.demo_running = False

        self.canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, font=("Helvetica", 13), pady=6)
        self.status.pack(fill="x")

        self._build_controls(root)
        self._snap_positions()
        self._render()
        self._set_status("Capacity 3. Put some keys, then Get one to see it jump to the front (MRU).")

    # -- controls -----------------------------------------------------------
    def _build_controls(self, root: tk.Tk) -> None:
        bar = tk.Frame(root)
        bar.pack(pady=8)

        tk.Label(bar, text="key").pack(side="left")
        self.key_entry = tk.Entry(bar, width=5)
        self.key_entry.pack(side="left", padx=(2, 8))
        tk.Label(bar, text="value").pack(side="left")
        self.val_entry = tk.Entry(bar, width=5)
        self.val_entry.pack(side="left", padx=(2, 12))

        tk.Button(bar, text="Put", command=self.on_put).pack(side="left", padx=4)
        tk.Button(bar, text="Get", command=self.on_get).pack(side="left", padx=4)
        tk.Button(bar, text="Run Demo", command=self.run_demo).pack(side="left", padx=12)
        tk.Button(bar, text="Reset", command=self.reset).pack(side="left", padx=4)

        tk.Label(bar, text="capacity").pack(side="left", padx=(12, 2))
        self.cap_spin = tk.Spinbox(bar, from_=1, to=MAX_CAP, width=3, command=self._change_capacity)
        self.cap_spin.delete(0, "end")
        self.cap_spin.insert(0, str(self.capacity))
        self.cap_spin.pack(side="left")

    def _set_status(self, text: str) -> None:
        self.status.config(text=text)

    def _read_int(self, entry: tk.Entry) -> int | None:
        try:
            return int(entry.get().strip())
        except ValueError:
            return None

    # -- button handlers ----------------------------------------------------
    def on_put(self) -> None:
        key, value = self._read_int(self.key_entry), self._read_int(self.val_entry)
        if key is None or value is None:
            self._set_status("Enter integer key AND value for Put.")
            return
        self._enqueue(("put", key, value))

    def on_get(self) -> None:
        key = self._read_int(self.key_entry)
        if key is None:
            self._set_status("Enter an integer key for Get.")
            return
        self._enqueue(("get", key))

    def _enqueue(self, op: tuple) -> None:
        """Queue an operation so clicks during an animation are honored, not dropped."""
        self.pending.append(op)
        if not self.animating:
            self._process_next()

    def run_demo(self) -> None:
        if self.animating or self.pending:
            return
        self.reset(capacity=3)
        self.demo_running = True
        self.pending = [
            ("put", 1, 10), ("put", 2, 20), ("put", 3, 30),
            ("get", 1),                      # hit -> 1 becomes MRU
            ("put", 4, 40),                  # full -> evicts LRU (key 2)
            ("get", 2),                      # miss -> -1
            ("put", 3, 99),                  # update existing -> moves to front
            ("get", 4),                      # hit
            ("put", 5, 50),                  # evicts LRU
        ]
        self.root.after(DEMO_PAUSE_MS, self._process_next)

    def reset(self, capacity: int | None = None) -> None:
        self.pending.clear()
        self.demo_running = False
        if self.animating:
            return  # halt any demo; cache rebuilds once the current animation ends
        if capacity is not None:
            self.capacity = capacity
            self.cap_spin.delete(0, "end")
            self.cap_spin.insert(0, str(capacity))
        self.cache = LRUCache(self.capacity)
        self.leaving.clear()
        self.highlight.clear()
        self.active_key = None
        self.pending.clear()
        self._snap_positions()
        self._render()
        self._set_status(f"Reset. Capacity = {self.capacity}.")

    def _change_capacity(self) -> None:
        try:
            cap = int(self.cap_spin.get())
        except ValueError:
            return
        self.reset(capacity=max(1, min(MAX_CAP, cap)))

    # -- apply one operation ------------------------------------------------
    def _apply(self, op: tuple) -> None:
        self.highlight.clear()
        self.leaving.clear()
        self.active_key = None

        if op[0] == "put":
            _, key, value = op
            event = self.cache.put(key, value)
            self._describe_put(event, key, value)
        else:
            _, key = op
            event = self.cache.get(key)
            self._describe_get(event, key)

        self._layout_targets()
        self._animate()

    def _describe_put(self, event: dict, key: int, value: int) -> None:
        self.active_key = key
        if event["type"] == "put_update":
            self.highlight[event["node"]] = HOT_HIT
            self._set_status(
                f"put({key},{value}): key exists -> update value, move to front (MRU). O(1)."
            )
        else:  # put_insert
            self.highlight[event["node"]] = HOT_NEW
            evicted = event["evicted"]
            if evicted is not None:
                self.highlight[evicted] = HOT_EVICT
                evicted.ty = -NODE_H
                self.leaving.append(evicted)
                self._set_status(
                    f"put({key},{value}): cache full -> insert at front AND evict LRU "
                    f"(key {evicted.key}, the tail). Removed from map too. O(1)."
                )
            else:
                self._set_status(
                    f"put({key},{value}): new key -> map insert + add at front (MRU). O(1)."
                )

    def _describe_get(self, event: dict, key: int) -> None:
        if event["type"] == "get_miss":
            self._set_status(f"get({key}): not in map -> return -1 (miss). O(1) lookup.")
        else:
            self.active_key = key
            self.highlight[event["node"]] = HOT_HIT
            self._set_status(
                f"get({key}): map gives the node in O(1) -> value {event['value']}, "
                f"move it to front (now MRU). O(1)."
            )

    def _next_pending(self) -> None:
        if not self.pending:
            self._set_status("Demo complete. Front = MRU, back = LRU. Every step was O(1).")
            return
        op = self.pending.pop(0)
        self._apply(op)

    # -- layout & animation -------------------------------------------------
    def _layout_targets(self) -> None:
        nodes = self.cache.real_nodes()
        self.cache.head.tx, self.cache.head.ty = DLL_LEFT, ROW_Y
        self.cache.tail.tx = DLL_LEFT + (len(nodes) + 1) * STEP
        self.cache.tail.ty = ROW_Y
        for i, n in enumerate(nodes):
            n.tx = DLL_LEFT + (i + 1) * STEP
            n.ty = ROW_Y

    def _snap_positions(self) -> None:
        self._layout_targets()
        for n in self._chain():
            n.x, n.y = n.tx, n.ty

    def _chain(self) -> list[Node]:
        return [self.cache.head, *self.cache.real_nodes(), self.cache.tail]

    def _animate(self) -> None:
        self.animating = True
        movers = self._chain() + self.leaving
        starts = {id(n): (n.x, n.y) for n in movers}
        self._step(movers, starts, 0)

    def _step(self, movers, starts, frame: int) -> None:
        t = _ease_out((frame + 1) / ANIM_FRAMES)
        for n in movers:
            sx, sy = starts[id(n)]
            n.x = sx + (n.tx - sx) * t
            n.y = sy + (n.ty - sy) * t
        self._render()
        if frame + 1 < ANIM_FRAMES:
            self.root.after(ANIM_INTERVAL_MS, self._step, movers, starts, frame + 1)
        else:
            self.leaving.clear()
            self.animating = False
            if self.pending:
                self.root.after(DEMO_PAUSE_MS, self._next_pending)

    # -- drawing ------------------------------------------------------------
    def _render(self) -> None:
        self.canvas.delete("all")
        self._draw_titles()
        map_rows = self._draw_hash_map()
        self._draw_dll()
        self._draw_connector(map_rows)
        self._draw_complexity()

    def _draw_titles(self) -> None:
        self.canvas.create_text(MAP_X, 70, text="HASH MAP  (key → node)", anchor="w",
                                font=("Helvetica", 13, "bold"), fill="#374151")
        self.canvas.create_text(DLL_LEFT, 70, text="DOUBLY LINKED LIST  (recency order)",
                                anchor="w", font=("Helvetica", 13, "bold"), fill="#374151")
        self.canvas.create_text(
            CANVAS_W - 30, 70,
            text=f"size {len(self.cache.map)} / capacity {self.capacity}",
            anchor="e", font=("Helvetica", 12), fill="#6b7280",
        )

    def _draw_hash_map(self) -> dict[int, float]:
        """Draw map rows sorted by key (stable). Returns key -> row center y."""
        rows: dict[int, float] = {}
        keys = sorted(self.cache.map.keys())
        if not keys:
            self.canvas.create_text(MAP_X, MAP_TOP + 10, text="(empty)", anchor="w",
                                    font=("Menlo", 12), fill="#9ca3af")
        for i, key in enumerate(keys):
            node = self.cache.map[key]
            y = MAP_TOP + i * MAP_ROW_H
            fill = "#fef3c7" if key == self.active_key else "#f9fafb"
            self.canvas.create_rectangle(MAP_X, y, MAP_X + MAP_W, y + MAP_ROW_H - 8,
                                         fill=fill, outline="#d1d5db")
            self.canvas.create_text(MAP_X + 12, y + (MAP_ROW_H - 8) / 2,
                                    text=f"{key}  →  node({node.key}:{node.value})",
                                    anchor="w", font=("Menlo", 12), fill="#111827")
            rows[key] = y + (MAP_ROW_H - 8) / 2
        return rows

    def _draw_dll(self) -> None:
        chain = self._chain()
        for a, b in zip(chain, chain[1:]):
            self._arrow(a.x + NODE_W / 4, min(a.y, b.y) - NODE_H / 2 - 9,
                        b.x - NODE_W / 4, min(a.y, b.y) - NODE_H / 2 - 9, NEXT_COLOR)
            self._arrow(b.x - NODE_W / 4, max(a.y, b.y) + NODE_H / 2 + 9,
                        a.x + NODE_W / 4, max(a.y, b.y) + NODE_H / 2 + 9, PREV_COLOR)
        for n in chain + self.leaving:
            self._draw_node(n)

    def _arrow(self, x1, y1, x2, y2, color) -> None:
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, arrow="last")

    def _draw_node(self, n: Node) -> None:
        if n.is_sentinel:
            fill, edge = SENTINEL_FILL, SENTINEL_EDGE
        else:
            fill = self.highlight.get(n, NODE_FILL)
            edge = NODE_EDGE
        x, y = n.x, n.y
        self.canvas.create_rectangle(x - NODE_W / 2, y - NODE_H / 2,
                                     x + NODE_W / 2, y + NODE_H / 2,
                                     fill=fill, outline=edge, width=2)
        font = ("Helvetica", 11, "bold") if n.is_sentinel else ("Helvetica", 15, "bold")
        self.canvas.create_text(x, y, text=n.text, font=font)

    def _draw_connector(self, map_rows: dict[int, float]) -> None:
        """Dashed line from the active key's map row to its node: the O(1) jump."""
        if self.active_key is None or self.active_key not in map_rows:
            return
        node = self.cache.map.get(self.active_key)
        if node is None:
            return
        y = map_rows[self.active_key]
        self.canvas.create_line(MAP_X + MAP_W, y, node.x - NODE_W / 2, node.y,
                                fill=LINK_COLOR, width=2, dash=(5, 3), arrow="last")

    def _draw_complexity(self) -> None:
        lines = [
            "get(key)  = map lookup O(1)  +  move-to-front O(1)  =  O(1)",
            "put(k,v)  = insert/update front O(1)  +  evict tail O(1)  =  O(1)",
            "front node = MRU (most recent)      back node = LRU (evicted next)",
        ]
        y0 = CANVAS_H - 78
        self.canvas.create_rectangle(20, y0 - 12, CANVAS_W - 20, CANVAS_H - 12,
                                     fill="#f9fafb", outline="#d1d5db")
        for i, line in enumerate(lines):
            self.canvas.create_text(36, y0 + i * 22, text=line, anchor="w",
                                    font=("Menlo", 12), fill="#374151")


def run() -> None:
    root = tk.Tk()
    LRUVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    run()
