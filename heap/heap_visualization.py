"""Animated binary heap / priority queue.

Run it:
    python heap/heap_visualization.py              # open the animation
    python heap/heap_visualization.py --selftest   # verify the model, print ok

What you'll see: the SAME heap drawn two ways at once.

    * TREE  (top)   : the conceptual view — a complete binary tree where every
                      parent beats both of its children.
    * ARRAY (middle): the actual storage. There are no node objects and no
                      pointers; the tree structure is pure index arithmetic.

That duality is the whole idea, and it is the thing to say out loud in an
interview. For the item at index `i`:

    parent(i) = (i - 1) // 2        left(i) = 2i + 1        right(i) = 2i + 2

Because a heap is *complete* (every level full except possibly the last, which
fills left to right), those formulas never leave a gap — so the array is dense
and the tree needs no pointers at all.

The heap invariant is deliberately weak: a parent beats its children, and that
is all. Siblings are unordered, and the array is NOT sorted. That weakness is
the point — maintaining it costs only O(log n) instead of the O(n) a sorted
array would need on every insert.

    push .......... O(log n)   append at the end, then sift UP
    pop ........... O(log n)   take the root, move the last item up, sift DOWN
    peek .......... O(1)       the answer is always at index 0
    heapify ....... O(n)       bottom-up sift-down; NOT O(n log n) — see below
    search ........ O(n)       a heap cannot find an arbitrary value quickly

Why heapify is O(n): sift-down cost is bounded by a node's HEIGHT, not the
tree's. Half the nodes are leaves (height 0 — free), a quarter have height 1,
and so on. The sum n/2*0 + n/4*1 + n/8*2 + ... converges to n, not n log n.

A priority queue is the interface ("give me the most urgent item"); a binary
heap is the usual implementation. Python's `heapq` is a MIN-heap over a plain
list — `heappush`, `heappop`, and `heap[0]` for peek. For a max-heap, negate
the priorities; `heapq` has no `reverse` flag.

Press "Drain" to pop everything: the served strip at the bottom comes out in
priority order, which is exactly the priority-queue guarantee. Note that this
is also heapsort — n pops at O(log n) each is O(n log n).
"""

from __future__ import annotations

import argparse
import random

# --- layout -----------------------------------------------------------------
CANVAS_W, CANVAS_H = 1180, 690
TREE_TOP = 96
LEVEL_H = 92
TREE_LEFT, TREE_RIGHT = 60, 1120
NODE_R = 26

ARRAY_Y = 470
CELL_W, CELL_H = 62, 46
ARRAY_LEFT = 60

SERVED_Y = 604
SERVED_LEFT = 168
SERVED_W = 46

MAX_ITEMS = 15  # 4 full levels — past this the tree stops being readable

# --- colors -----------------------------------------------------------------
BG = "#f8fafc"
NODE_FILL = "#dbeafe"
NODE_EDGE = "#1d4ed8"
HOT_COMPARE = "#fde68a"  # the two items being compared right now
HOT_SWAP = "#fecaca"     # items about to trade places
HOT_ROOT = "#bbf7d0"     # the winner sitting at index 0
HOT_NEW = "#e9d5ff"      # freshly appended, not yet sifted
EDGE_COLOR = "#94a3b8"
CELL_FILL = "#ffffff"
CELL_EDGE = "#cbd5e1"
SERVED_FILL = "#dcfce7"
SERVED_EDGE = "#16a34a"
TEXT = "#0f172a"
MUTED = "#64748b"

ANIM_FRAMES = 16
ANIM_INTERVAL_MS = 16
STEP_PAUSE_MS = 340


class Item:
    """One heap entry: a priority plus a task label, and its on-screen position.

    Model and view state share a class to keep this a single readable file; in
    production they would obviously be separate.
    """

    def __init__(self, priority: int, name: str):
        self.priority = priority
        self.name = name
        # current and target positions: [tree_x, tree_y, array_x]
        self.pos = [0.0, 0.0, 0.0]
        self.target = [0.0, 0.0, 0.0]

    def __repr__(self) -> str:  # helps when debugging the model in a REPL
        return f"Item({self.priority}, {self.name!r})"


class Step:
    """One frame of narration: an array ordering plus what to highlight."""

    def __init__(self, order, caption, compare=(), swap=(), new=(), settled=False):
        self.order = list(order)
        self.caption = caption
        self.compare = set(compare)
        self.swap = set(swap)
        self.new = set(new)
        self.settled = settled


def tree_position(index: int) -> tuple[float, float]:
    """Where item `index` sits in the tree drawing.

    Depth is floor(log2(index + 1)); the slot within that level is
    index - (2**depth - 1). Each level is spread evenly across the canvas, so a
    complete tree always looks balanced.
    """
    depth = 0
    while (1 << (depth + 1)) - 1 <= index:
        depth += 1
    first = (1 << depth) - 1
    slot = index - first
    width = TREE_RIGHT - TREE_LEFT
    span = width / (1 << depth)
    x = TREE_LEFT + span * (slot + 0.5)
    y = TREE_TOP + depth * LEVEL_H
    return x, y


def array_position(index: int) -> float:
    return ARRAY_LEFT + index * CELL_W + CELL_W / 2


class HeapModel:
    """The heap itself, plus a recording of every comparison and swap.

    Every mutating operation appends `Step`s to `self.steps`; the view replays
    them. Keeping this free of tkinter means the logic is testable — see
    `run_selftest`.
    """

    def __init__(self, is_min: bool = True):
        self.items: list[Item] = []
        self.is_min = is_min
        self.steps: list[Step] = []
        self.served: list[Item] = []
        self._counter = 0

    # --- helpers ------------------------------------------------------------

    def _beats(self, a: Item, b: Item) -> bool:
        """Does `a` have priority over `b` under the current heap order?"""
        return a.priority < b.priority if self.is_min else a.priority > b.priority

    def _word(self) -> str:
        return "smallest" if self.is_min else "largest"

    def _record(self, caption, compare=(), swap=(), new=(), settled=False) -> None:
        self.steps.append(Step(self.items, caption, compare, swap, new, settled))

    def next_name(self) -> str:
        self._counter += 1
        return f"job{self._counter}"

    # --- operations ---------------------------------------------------------

    def push(self, priority: int, name: str | None = None) -> None:
        """Append at the end, then sift up until the parent beats us."""
        if len(self.items) >= MAX_ITEMS:
            self._record(f"Capacity {MAX_ITEMS} reached — pop something first.")
            return
        item = Item(priority, name or self.next_name())
        self.items.append(item)
        i = len(self.items) - 1
        self._record(
            f"push({priority}): append at index {i} — the only spot that keeps "
            f"the tree complete. Now sift UP.",
            new=(i,),
        )
        while i > 0:
            parent = (i - 1) // 2
            self._record(
                f"Compare index {i} ({self.items[i].priority}) with parent "
                f"({i} - 1) // 2 = {parent} ({self.items[parent].priority}).",
                compare=(i, parent),
            )
            if not self._beats(self.items[i], self.items[parent]):
                self._record(
                    f"Parent already wins — invariant holds. Done in "
                    f"{self._depth_of(i)} level(s), O(log n).",
                    settled=True,
                )
                return
            self._record(
                f"{self.items[i].priority} beats {self.items[parent].priority} — swap up.",
                swap=(i, parent),
            )
            self.items[i], self.items[parent] = self.items[parent], self.items[i]
            i = parent
        self._record(
            f"Reached the root — {self.items[0].priority} is now the "
            f"{self._word()} priority.",
            settled=True,
        )

    def pop(self) -> Item | None:
        """Take index 0, move the last item into it, then sift down."""
        if not self.items:
            self._record("pop() on an empty heap — nothing to serve.")
            return None
        winner = self.items[0]
        self._record(
            f"pop(): the root is always the {self._word()} — serve "
            f"{winner.priority} ({winner.name}).",
            compare=(0,),
        )
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            self._record(
                f"Move the LAST item ({last.priority}) into the root. The tree "
                f"stays complete, but the invariant is broken — sift DOWN.",
                new=(0,),
            )
        else:
            self._record("That was the last item — the heap is now empty.", settled=True)
            self.served.append(winner)
            return winner

        i = 0
        n = len(self.items)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            best = i
            children = [c for c in (left, right) if c < n]
            if not children:
                self._record(
                    f"Index {i} is a leaf — nowhere left to sink. Done, O(log n).",
                    settled=True,
                )
                break
            shown = " and ".join(f"{c} ({self.items[c].priority})" for c in children)
            self._record(
                f"Compare index {i} ({self.items[i].priority}) with child {shown}.",
                compare=(i, *children),
            )
            for child in children:
                if self._beats(self.items[child], self.items[best]):
                    best = child
            if best == i:
                self._record(
                    "Parent beats both children — invariant restored.", settled=True
                )
                break
            self._record(
                f"Child {best} ({self.items[best].priority}) wins — swap down. "
                f"Always pick the better CHILD, or you break the other subtree.",
                swap=(i, best),
            )
            self.items[i], self.items[best] = self.items[best], self.items[i]
            i = best
        self.served.append(winner)
        return winner

    def peek(self) -> Item | None:
        if not self.items:
            self._record("peek() on an empty heap.")
            return None
        top = self.items[0]
        self._record(
            f"peek() = {top.priority} ({top.name}) — index 0, no traversal, O(1).",
            compare=(0,),
            settled=True,
        )
        return top

    def heapify(self, priorities: list[int]) -> None:
        """Bottom-up build: sift down every internal node, last to first.

        Leaves are already valid heaps of size one, so start at the last parent
        at index n // 2 - 1 and walk backwards.
        """
        self.items = [Item(p, self.next_name()) for p in priorities[:MAX_ITEMS]]
        n = len(self.items)
        self._record(
            f"heapify(): dropped {n} unordered items into the array. Every index "
            f">= {n // 2} is a leaf, so it is already a valid heap of size 1.",
        )
        for start in range(n // 2 - 1, -1, -1):
            self._record(
                f"Sift down from index {start} ({self.items[start].priority}) — "
                f"walking backwards so children are fixed before their parent.",
                compare=(start,),
            )
            i = start
            while True:
                left, right = 2 * i + 1, 2 * i + 2
                best = i
                for child in (left, right):
                    if child < n and self._beats(self.items[child], self.items[best]):
                        best = child
                if best == i:
                    break
                self._record(
                    f"Swap index {i} ({self.items[i].priority}) with "
                    f"{best} ({self.items[best].priority}).",
                    swap=(i, best),
                )
                self.items[i], self.items[best] = self.items[best], self.items[i]
                i = best
        self._record(
            "Heap built. This is O(n), not O(n log n): sift-down cost is bounded "
            "by each node's HEIGHT, and half the nodes are leaves with height 0.",
            settled=True,
        )

    def clear(self) -> None:
        self.items.clear()
        self.served.clear()
        self._record("Cleared.", settled=True)

    def _depth_of(self, index: int) -> int:
        depth = 0
        while index > 0:
            index = (index - 1) // 2
            depth += 1
        return depth

    def is_valid(self) -> bool:
        """Check the heap invariant directly — used by the self-test."""
        for i in range(1, len(self.items)):
            if self._beats(self.items[i], self.items[(i - 1) // 2]):
                return False
        return True


# --------------------------------------------------------------------------
# View
# --------------------------------------------------------------------------


def launch() -> None:
    import tkinter as tk

    model = HeapModel(is_min=True)
    root = tk.Tk()
    root.title("Binary Heap / Priority Queue")
    root.configure(bg=BG)
    # Launched from a terminal the window otherwise opens behind it.
    root.lift()
    root.attributes("-topmost", True)
    root.after(400, lambda: root.attributes("-topmost", False))

    canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg=BG, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=9, padx=10, pady=(10, 4))

    state = {"playing": False, "queue": [], "caption": "Push a priority to begin."}

    # --- drawing ----------------------------------------------------------

    def layout_targets(order: list[Item]) -> None:
        for index, item in enumerate(order):
            tx, ty = tree_position(index)
            item.target = [tx, ty, array_position(index)]

    def snap(order: list[Item]) -> None:
        layout_targets(order)
        for item in order:
            item.pos = list(item.target)

    def fill_for(index: int, step: Step | None) -> str:
        if step is None:
            return HOT_ROOT if index == 0 else NODE_FILL
        if index in step.swap:
            return HOT_SWAP
        if index in step.new:
            return HOT_NEW
        if index in step.compare:
            return HOT_COMPARE
        if index == 0 and step.settled:
            return HOT_ROOT
        return NODE_FILL

    def draw(order: list[Item], step: Step | None) -> None:
        canvas.delete("all")
        mode = "MIN-heap" if model.is_min else "MAX-heap"
        canvas.create_text(
            20, 22, anchor="w", text=f"{mode} — parent beats both children",
            font=("Helvetica", 16, "bold"), fill=TEXT,
        )
        canvas.create_text(
            20, 46, anchor="w",
            text="parent(i) = (i-1)//2     left(i) = 2i+1     right(i) = 2i+2"
                 "     peek O(1) · push/pop O(log n) · heapify O(n)",
            font=("Courier", 12), fill=MUTED,
        )

        # tree edges first, so nodes draw on top
        for index in range(len(order)):
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(order):
                    canvas.create_line(
                        order[index].pos[0], order[index].pos[1],
                        order[child].pos[0], order[child].pos[1],
                        fill=EDGE_COLOR, width=2,
                    )

        for index, item in enumerate(order):
            x, y = item.pos[0], item.pos[1]
            canvas.create_oval(
                x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R,
                fill=fill_for(index, step), outline=NODE_EDGE, width=2,
            )
            canvas.create_text(x, y - 4, text=str(item.priority),
                               font=("Helvetica", 15, "bold"), fill=TEXT)
            canvas.create_text(x, y + 12, text=item.name,
                               font=("Helvetica", 7), fill=MUTED)
            canvas.create_text(x + NODE_R + 2, y - NODE_R + 2, text=f"[{index}]",
                               font=("Courier", 9), fill=MUTED, anchor="w")

        # array view
        canvas.create_text(
            ARRAY_LEFT, ARRAY_Y - CELL_H, anchor="w",
            text="the actual storage — one flat list, no pointers:",
            font=("Helvetica", 11, "italic"), fill=MUTED,
        )
        for index in range(max(len(order), 1)):
            left = ARRAY_LEFT + index * CELL_W
            canvas.create_rectangle(
                left, ARRAY_Y - CELL_H / 2, left + CELL_W, ARRAY_Y + CELL_H / 2,
                fill=CELL_FILL, outline=CELL_EDGE,
            )
            canvas.create_text(left + CELL_W / 2, ARRAY_Y + CELL_H / 2 + 12,
                               text=str(index), font=("Courier", 10), fill=MUTED)
        for index, item in enumerate(order):
            x = item.pos[2]
            canvas.create_rectangle(
                x - CELL_W / 2 + 3, ARRAY_Y - CELL_H / 2 + 3,
                x + CELL_W / 2 - 3, ARRAY_Y + CELL_H / 2 - 3,
                fill=fill_for(index, step), outline=NODE_EDGE, width=2,
            )
            canvas.create_text(x, ARRAY_Y, text=str(item.priority),
                               font=("Helvetica", 13, "bold"), fill=TEXT)

        # served strip
        canvas.create_text(
            20, SERVED_Y, anchor="w", text="served (pop order):",
            font=("Helvetica", 11, "bold"), fill=TEXT,
        )
        if not model.served:
            canvas.create_text(SERVED_LEFT, SERVED_Y, anchor="w",
                               text="— nothing popped yet —",
                               font=("Helvetica", 10, "italic"), fill=MUTED)
        for order_index, item in enumerate(model.served[-18:]):
            left = SERVED_LEFT + order_index * SERVED_W
            canvas.create_rectangle(left, SERVED_Y - 16, left + SERVED_W - 6,
                                    SERVED_Y + 16, fill=SERVED_FILL,
                                    outline=SERVED_EDGE)
            canvas.create_text(left + (SERVED_W - 6) / 2, SERVED_Y,
                               text=str(item.priority),
                               font=("Helvetica", 12, "bold"), fill=TEXT)

        canvas.create_text(
            20, CANVAS_H - 22, anchor="w", text=state["caption"],
            font=("Helvetica", 12), fill=TEXT, width=CANVAS_W - 40,
        )

    # --- playback ---------------------------------------------------------

    def play_next() -> None:
        if not state["queue"]:
            state["playing"] = False
            layout_targets(model.items)
            snap(model.items)
            draw(model.items, None)
            return
        step = state["queue"].pop(0)
        state["caption"] = step.caption
        layout_targets(step.order)
        animate(step, 0)

    def animate(step: Step, frame: int) -> None:
        if frame > ANIM_FRAMES:
            for item in step.order:  # land exactly on target, no drift
                item.pos = list(item.target)
            draw(step.order, step)
            root.after(STEP_PAUSE_MS, play_next)
            return
        t = frame / ANIM_FRAMES
        eased = t * t * (3 - 2 * t)  # smoothstep
        for item in step.order:
            for axis in range(3):
                start = item.pos[axis]
                item.pos[axis] = start + (item.target[axis] - start) * eased * 0.55
        draw(step.order, step)
        root.after(ANIM_INTERVAL_MS, lambda: animate(step, frame + 1))

    def run(action) -> None:
        """Execute a model action and queue its recorded steps for playback."""
        if state["playing"]:
            return
        model.steps.clear()
        action()
        if not model.steps:
            return
        snap(model.steps[0].order)
        state["queue"] = list(model.steps)
        state["playing"] = True
        play_next()

    # --- controls ---------------------------------------------------------

    entry = None  # assigned below; referenced by do_push

    def do_push() -> None:
        raw = entry.get().strip()
        try:
            priority = int(raw)
        except ValueError:
            priority = random.randint(1, 99)
            entry.delete(0, "end")
            entry.insert(0, str(priority))
        run(lambda: model.push(priority))

    def do_drain() -> None:
        if state["playing"] or not model.items:
            return
        model.steps.clear()
        while model.items:
            model.pop()
        snap(model.steps[0].order)
        state["queue"] = list(model.steps)
        state["playing"] = True
        play_next()

    def do_heapify() -> None:
        sample = random.sample(range(1, 99), random.randint(7, 12))
        run(lambda: model.heapify(sample))

    def toggle_mode() -> None:
        if state["playing"]:
            return
        model.is_min = not model.is_min
        mode_button.config(text="MIN-heap" if model.is_min else "MAX-heap")
        run(lambda: model.heapify([i.priority for i in model.items]))

    bar = tk.Frame(root, bg=BG)
    bar.grid(row=1, column=0, columnspan=9, pady=(0, 12))

    tk.Label(bar, text="priority:", bg=BG, fg=TEXT).pack(side="left", padx=(0, 4))
    entry = tk.Entry(bar, width=6)
    entry.pack(side="left", padx=(0, 8))
    entry.insert(0, "42")

    def button(text, command):
        tk.Button(bar, text=text, command=command, width=11).pack(side="left", padx=3)

    button("Push", do_push)
    button("Pop", lambda: run(model.pop))
    button("Peek", lambda: run(model.peek))
    button("Heapify", do_heapify)
    button("Drain", do_drain)
    button("Clear", lambda: run(model.clear))
    mode_button = tk.Button(bar, text="MIN-heap", command=toggle_mode, width=11)
    mode_button.pack(side="left", padx=3)

    for priority in (52, 31, 74, 18, 66):
        model.push(priority)
    model.steps.clear()
    snap(model.items)
    draw(model.items, None)
    root.mainloop()


# --------------------------------------------------------------------------
# Self-test — verifies the model without opening a window
# --------------------------------------------------------------------------


def run_selftest() -> None:
    import heapq

    # push keeps the min-heap invariant, and the root matches heapq
    model = HeapModel(is_min=True)
    reference: list[int] = []
    for priority in [52, 31, 74, 18, 66, 5, 99, 41]:
        model.push(priority)
        heapq.heappush(reference, priority)
        assert model.is_valid(), f"invariant broken after push({priority})"
        assert model.items[0].priority == reference[0]

    # popping drains in sorted order — the priority-queue guarantee
    popped = []
    while model.items:
        popped.append(model.pop().priority)
        assert model.is_valid(), "invariant broken after pop"
    assert popped == sorted([52, 31, 74, 18, 66, 5, 99, 41]), popped
    assert model.pop() is None  # empty pop is a no-op, not a crash

    # max-heap mode inverts the order
    model = HeapModel(is_min=False)
    for priority in [3, 9, 1, 7]:
        model.push(priority)
    assert model.items[0].priority == 9
    assert [model.pop().priority for _ in range(4)] == [9, 7, 3, 1]

    # heapify produces a valid heap from arbitrary input
    model = HeapModel(is_min=True)
    values = [9, 4, 7, 1, 8, 2, 6, 3]
    model.heapify(values)
    assert model.is_valid()
    assert model.items[0].priority == 1
    assert sorted(i.priority for i in model.items) == sorted(values)

    # index arithmetic matches the drawing: children sit one level below
    for index in range(1, MAX_ITEMS):
        _, parent_y = tree_position((index - 1) // 2)
        _, child_y = tree_position(index)
        assert child_y - parent_y == LEVEL_H, index

    # every step records a caption, so the narration can never go blank
    assert all(step.caption for step in model.steps)

    print("ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true",
                        help="verify the heap model without opening a window")
    if parser.parse_args().selftest:
        run_selftest()
    else:
        launch()
