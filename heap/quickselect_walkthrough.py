"""Step-through walkthrough of quickselect — the kth largest WITHOUT a heap.

Run it:
    python heap/quickselect_walkthrough.py              # open the walkthrough
    python heap/quickselect_walkthrough.py --selftest   # verify, print ok

Companion to `heapify_walkthrough.py`. Both answer "give me the kth largest";
this one does it in O(n) average time and O(1) extra space, beating both the
O(n log n) sort and the O(n log k) bounded heap.

    Next / Right arrow ...... advance one step
    Back / Left arrow ....... rewind one step
    Play / Space ............ auto-advance until paused again
    New array ............... fresh random values and a fresh pivot sequence

THE IDEA — quicksort with the recursion halved.

Partitioning around a pivot puts that pivot in its FINAL sorted position: every
smaller value ends up to its left, every larger to its right. That index is now
known and permanent, so compare it to the index you are hunting and throw away
the side that cannot contain the answer.

    pivot index == target  ->  done
    pivot index <  target  ->  answer is to the right, discard the left
    pivot index >  target  ->  answer is to the left,  discard the right

Quicksort recurses into BOTH halves, which is where its n log n comes from.
Quickselect discards one half every round:

    n + n/2 + n/4 + n/8 + ...  ->  2n  =  O(n)

The rounds panel in the window draws that shrinking window so you can see the
series collapse rather than take it on faith.

TWO DETAILS THAT DECIDE CORRECTNESS

  * The target index. For the kth LARGEST in an array partitioned ascending,
    target = len(a) - k. Check it against k = 1 (last index) and k = n (index
    0); an off-by-one here is the most common quickselect bug.
  * The pivot. A fixed pivot (first or last element) degrades to O(n^2) on
    already-sorted input, and that adversarial case is in LeetCode's test suite
    for this problem, so the naive version times out. A random pivot fixes it in
    practice. Median-of-medians guarantees O(n) worst case but has constants bad
    enough that nobody ships it — know the name, don't write it.

This uses Lomuto partitioning: park the pivot at the end, sweep a scan pointer
across the window, and keep a `store` boundary marking where the next
smaller-than-pivot value belongs. Hoare's scheme does fewer swaps but is fiddlier
to get right under pressure.

The array is partially reordered in place — that is the price of O(1) space, and
worth saying out loud, since callers rarely expect their input to be rearranged.
"""

from __future__ import annotations

import argparse
import random

# --- layout -----------------------------------------------------------------
CANVAS_W, CANVAS_H = 1520, 712

ARRAY_LEFT = 60
ARRAY_Y = 214
CELL_W, CELL_H = 62, 54
BRACKET_Y = 150
INDEX_Y = 252
TARGET_Y = 284

ROUNDS_LEFT = 60
ROUNDS_TOP = 330
ROUNDS_RIGHT = 852
ROUNDS_BAR_H = 18

PANEL_LEFT = 40
PANEL_TOP = 464
PANEL_RIGHT = 852

CODE_LEFT = 884
CODE_TOP = 96
CODE_LINE_H = 23
CODE_RIGHT = 1506

MAX_ITEMS = 12

# --- colors -----------------------------------------------------------------
BG = "#f8fafc"
CELL_FILL = "#ffffff"
CELL_EDGE = "#94a3b8"
DISCARD_FILL = "#f1f5f9"   # outside the live window — provably not the answer
DISCARD_EDGE = "#e2e8f0"
DISCARD_TEXT = "#cbd5e1"
PIVOT_FILL = "#ddd6fe"
PIVOT_EDGE = "#7c3aed"
CURSOR_FILL = "#bfdbfe"    # the scan pointer i
CURSOR_EDGE = "#1d4ed8"
LESS_FILL = "#fed7aa"      # proven smaller than the pivot
LESS_EDGE = "#ea580c"
SWAP_FILL = "#fecaca"
FOUND_FILL = "#bbf7d0"
FOUND_EDGE = "#16a34a"
TARGET_MARK = "#dc2626"
BAR_FILL = "#93c5fd"
BAR_EDGE = "#1d4ed8"
CODE_BG = "#0f172a"
CODE_FG = "#e2e8f0"
CODE_DIM = "#64748b"
CODE_HL = "#1e3a5f"
CODE_HL_FG = "#fef3c7"
PANEL_BG = "#ffffff"
PANEL_EDGE = "#cbd5e1"
TEXT = "#0f172a"
MUTED = "#64748b"
ACCENT = "#b45309"

ANIM_FRAMES = 12
ANIM_INTERVAL_MS = 16
AUTOPLAY_MS = 900

CODE = [
    "def quickselect(a, k):",
    "    target = len(a) - k      # kth largest",
    "    lo, hi = 0, len(a) - 1",
    "    while True:",
    "        if lo == hi:",
    "            return a[lo]",
    "        p = partition(a, lo, hi)",
    "        if p == target:",
    "            return a[p]",
    "        elif p < target:",
    "            lo = p + 1       # discard the left",
    "        else:",
    "            hi = p - 1       # discard the right",
    "",
    "def partition(a, lo, hi):",
    "    pivot_i = random.randint(lo, hi)",
    "    a[pivot_i], a[hi] = a[hi], a[pivot_i]",
    "    store = lo",
    "    for i in range(lo, hi):",
    "        if a[i] < a[hi]:",
    "            a[store], a[i] = a[i], a[store]",
    "            store += 1",
    "    a[store], a[hi] = a[hi], a[store]",
    "    return store",
]


class Item:
    """One array cell. Stable identity so swaps can be animated."""

    def __init__(self, value: int):
        self.value = value
        self.pos = 0.0
        self.target = 0.0

    def __repr__(self) -> str:
        return f"Item({self.value})"


class Step:
    def __init__(self, order, code_line, title, detail, roles, marks, stats, rounds):
        self.order = list(order)
        self.code_line = code_line
        self.title = title
        self.detail = detail
        self.roles = dict(roles)
        self.marks = dict(marks)    # lo / hi / target / store / pivot / answer
        self.stats = dict(stats)
        self.rounds = list(rounds)  # (round_number, window_size) completed


def array_position(index: int) -> float:
    return ARRAY_LEFT + index * CELL_W + CELL_W / 2


def build_steps(values: list[int], k: int, seed: int = 0) -> list[Step]:
    """Run quickselect on `values`, recording a narrated Step at each decision."""
    items = [Item(v) for v in values[:MAX_ITEMS]]
    n = len(items)
    if not 1 <= k <= n:
        raise ValueError(f"k must be in 1..{n}, got {k}")

    rng = random.Random(seed)
    steps: list[Step] = []
    stats = {"comparisons": 0, "swaps": 0, "scanned": 0, "rounds": 0}
    rounds: list[tuple[int, int]] = []
    target = n - k

    def add(code_line, title, detail, roles=None, marks=None):
        steps.append(Step(items, code_line, title, detail, roles or {},
                          marks or {}, stats, rounds))

    def outside(lo: int, hi: int) -> dict[int, str]:
        return {i: "discard" for i in range(n) if i < lo or i > hi}

    add(
        1,
        f"Goal: the {k}th largest of {n} values",
        [
            f"Sorted descending, the answer sits at position {k}. Sorted "
            f"ASCENDING — which is how partitioning arranges things — that is "
            f"index target = n - k = {n} - {k} = {target}.",
            "Getting this index wrong is the classic quickselect bug. Sanity "
            f"check: k = 1 would give index {n - 1} (the last), k = {n} would "
            "give index 0.",
            "We never sort. We only need whichever value ends up at that one "
            "index.",
        ],
        marks={"target": target},
    )

    lo, hi = 0, n - 1
    while True:
        stats["rounds"] += 1
        window = hi - lo + 1
        add(
            3,
            f"Round {stats['rounds']}: live window is [{lo}..{hi}], {window} "
            f"element{'s' if window != 1 else ''}",
            [
                f"Everything outside [{lo}..{hi}] is greyed out — already proven "
                "to be on the wrong side of the answer, and never looked at again.",
                "Each round throws away part of the array, which is why the total "
                "work is n + n/2 + n/4 + ... = 2n rather than n log n.",
            ],
            {**outside(lo, hi)},
            {"lo": lo, "hi": hi, "target": target},
        )

        if lo == hi:
            add(
                5,
                f"Window is one element — that must be the answer: {items[lo].value}",
                [
                    f"lo == hi == {lo}, and we know the answer lies inside the "
                    "window, so no partition is needed.",
                ],
                {**outside(lo, hi), lo: "found"},
                {"lo": lo, "hi": hi, "target": target, "answer": lo},
            )
            break

        pivot_index = rng.randint(lo, hi)
        add(
            15,
            f"Pick a RANDOM pivot: index {pivot_index} (value {items[pivot_index].value})",
            [
                "Random, not first or last. A fixed pivot degrades to O(n^2) on "
                "sorted input, and that case is in the judge's test suite.",
                "Randomising makes the bad case astronomically unlikely rather "
                "than reliably triggerable by the input.",
            ],
            {**outside(lo, hi), pivot_index: "pivot"},
            {"lo": lo, "hi": hi, "target": target, "pivot": pivot_index},
        )

        items[pivot_index], items[hi] = items[hi], items[pivot_index]
        stats["swaps"] += 1
        pivot_value = items[hi].value
        add(
            16,
            f"Park the pivot at the end (index {hi})",
            [
                "Moving it out of the way means the scan has a clean run of "
                "cells to sweep and the pivot cannot be swapped with itself "
                "mid-loop.",
                f"Pivot value is {pivot_value}. Everything smaller will be "
                "herded to the left.",
            ],
            {**outside(lo, hi), hi: "pivot"},
            {"lo": lo, "hi": hi, "target": target, "pivot": hi},
        )

        store = lo
        add(
            17,
            f"store = {store}: the boundary of the 'smaller than pivot' region",
            [
                "`store` always points at the slot where the NEXT value smaller "
                "than the pivot belongs.",
                f"Invariant: everything in [{lo}..store-1] is < pivot. Right now "
                "that range is empty, so it holds trivially.",
            ],
            {**outside(lo, hi), hi: "pivot"},
            {"lo": lo, "hi": hi, "target": target, "pivot": hi, "store": store},
        )

        for i in range(lo, hi):
            stats["comparisons"] += 1
            stats["scanned"] += 1
            smaller = items[i].value < pivot_value
            less_region = {j: "less" for j in range(lo, store)}
            add(
                19,
                f"i = {i}: is {items[i].value} < {pivot_value}?  "
                f"{'yes' if smaller else 'no'}",
                [
                    f"Compare a[{i}] with the pivot."
                    + (f" It is smaller, so it belongs in the left region — swap "
                       f"it to index {store} and push the boundary out."
                       if smaller else
                       " It is not smaller, so leave it where it is; the scan "
                       "pointer moves on but the boundary does not."),
                ],
                {**outside(lo, hi), **less_region, hi: "pivot", i: "cursor"},
                {"lo": lo, "hi": hi, "target": target, "pivot": hi, "store": store},
            )
            if smaller:
                if store != i:
                    items[store], items[i] = items[i], items[store]
                    stats["swaps"] += 1
                store += 1
                add(
                    21,
                    f"store advances to {store}",
                    [
                        f"Everything in [{lo}..{store - 1}] is now known to be "
                        "smaller than the pivot.",
                    ],
                    {**outside(lo, hi),
                     **{j: "less" for j in range(lo, store)}, hi: "pivot"},
                    {"lo": lo, "hi": hi, "target": target, "pivot": hi,
                     "store": store},
                )

        items[store], items[hi] = items[hi], items[store]
        stats["swaps"] += 1
        add(
            22,
            f"Swap the pivot into index {store} — its FINAL sorted position",
            [
                f"Everything left of {store} is smaller, everything right is not. "
                f"No matter what happens next, {pivot_value} belongs at index "
                f"{store} in the fully sorted array.",
                "That permanence is the whole trick: one partition pass buys us "
                "one exact, final index.",
            ],
            {**outside(lo, hi),
             **{j: "less" for j in range(lo, store)}, store: "pivot"},
            {"lo": lo, "hi": hi, "target": target, "pivot": store,
             "store": store},
        )
        rounds.append((stats["rounds"], window))

        if store == target:
            add(
                8,
                f"p == target ({store}) — the answer is {items[store].value}",
                [
                    f"The pivot landed exactly on the index we were hunting, so "
                    f"a[{store}] = {items[store].value} is the {k}th largest.",
                    "Note the rest of the array is still unsorted, and that is "
                    "fine — we never needed it.",
                ],
                {**outside(lo, hi), store: "found"},
                {"lo": lo, "hi": hi, "target": target, "answer": store},
            )
            break

        if store < target:
            add(
                10,
                f"p = {store} < target = {target} — discard the left, keep [{store + 1}..{hi}]",
                [
                    f"The answer sits at a HIGHER index than the pivot, so every "
                    f"cell from {lo} to {store} is eliminated in one stroke — "
                    f"{store - lo + 1} of them.",
                    "We do not recurse into the discarded side. That is the only "
                    "difference from quicksort, and it is what turns n log n "
                    "into n.",
                ],
                {**outside(lo, hi),
                 **{j: "discard" for j in range(lo, store + 1)}},
                {"lo": store + 1, "hi": hi, "target": target},
            )
            lo = store + 1
        else:
            add(
                12,
                f"p = {store} > target = {target} — discard the right, keep [{lo}..{store - 1}]",
                [
                    f"The answer sits at a LOWER index than the pivot, so cells "
                    f"{store} to {hi} are eliminated — {hi - store + 1} of them.",
                    "Again, only one side survives.",
                ],
                {**outside(lo, hi),
                 **{j: "discard" for j in range(store, hi + 1)}},
                {"lo": lo, "hi": store - 1, "target": target},
            )
            hi = store - 1

    answer = steps[-1].marks["answer"]
    total = sum(size for _, size in rounds) or n
    add(
        0,
        f"Answer: {items[answer].value} — the {k}th largest",
        [
            f"Final array: {[item.value for item in items]}",
            f"Still not sorted — and it did not need to be. Only index "
            f"{target} is guaranteed correct.",
            f"{stats['rounds']} round(s), {stats['comparisons']} comparisons, "
            f"{stats['swaps']} swaps. Window sizes were "
            f"{[size for _, size in rounds] or [n]}, summing to {total} for "
            f"n = {n} — that is the n + n/2 + n/4 + ... < 2n series, so O(n).",
            "Average O(n), worst O(n^2) if pivots land badly every round; the "
            "random pivot makes that vanishingly unlikely. O(1) extra space, but "
            "the input is reordered in place.",
        ],
        {answer: "found"},
        {"target": target, "answer": answer},
    )
    return steps


# --------------------------------------------------------------------------
# View
# --------------------------------------------------------------------------


def launch(values: list[int] | None = None, k: int | None = None,
           seed: int = 0) -> None:
    import tkinter as tk

    state = {
        "values": values or random.sample(range(1, 99), 10),
        "k": k or 4,
        "seed": seed,
        "steps": [],
        "index": 0,
        "playing": False,
        "animating": False,
        "scale": 1.0,
    }

    root = tk.Tk()
    root.title("Quickselect — step by step")
    root.configure(bg=BG)
    root.lift()
    root.attributes("-topmost", True)
    root.after(400, lambda: root.attributes("-topmost", False))

    start_scale = min(
        1.0,
        (root.winfo_screenwidth() - 60) / CANVAS_W,
        (root.winfo_screenheight() - 170) / CANVAS_H,
    )
    state["scale"] = start_scale

    def s(value: float) -> float:
        return value * state["scale"]

    def font(size: int, weight: str = "normal", family: str = "Helvetica"):
        return (family, max(6, int(size * state["scale"])), weight)

    def mono(size: int, weight: str = "normal"):
        return font(size, weight, "Courier")

    canvas = tk.Canvas(root, width=int(CANVAS_W * start_scale),
                       height=int(CANVAS_H * start_scale), bg=BG,
                       highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 4))
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # --- geometry ---------------------------------------------------------

    def layout(order: list[Item]) -> None:
        for index, item in enumerate(order):
            item.target = array_position(index)

    def snap(order: list[Item]) -> None:
        layout(order)
        for item in order:
            item.pos = item.target

    # --- drawing ----------------------------------------------------------

    def style_for(index: int, step: Step) -> tuple[str, str, str]:
        role = step.roles.get(index)
        if role == "found":
            return FOUND_FILL, FOUND_EDGE, TEXT
        if role == "pivot":
            return PIVOT_FILL, PIVOT_EDGE, TEXT
        if role == "cursor":
            return CURSOR_FILL, CURSOR_EDGE, TEXT
        if role == "less":
            return LESS_FILL, LESS_EDGE, TEXT
        if role == "discard":
            return DISCARD_FILL, DISCARD_EDGE, DISCARD_TEXT
        return CELL_FILL, CELL_EDGE, TEXT

    def draw(step: Step, attempt: int = 0) -> None:
        canvas.delete("all")
        order = step.order
        n = len(order)
        cell_w, cell_h = s(CELL_W), s(CELL_H)

        canvas.create_text(s(22), s(24), anchor="w",
                           text="quickselect — kth largest in O(n), no heap",
                           font=font(17, "bold"), fill=TEXT)
        canvas.create_text(
            s(22), s(48), anchor="w",
            text="partition puts the pivot at its FINAL index, then we keep only "
                 "the side that can hold the answer",
            font=mono(11), fill=MUTED)
        canvas.create_text(
            s(22), s(70), anchor="w",
            text=f"step {state['index'] + 1} / {len(state['steps'])}"
                 f"     round {step.stats['rounds']}"
                 f"     comparisons {step.stats['comparisons']}"
                 f"     swaps {step.stats['swaps']}",
            font=mono(11, "bold"), fill=ACCENT)

        lo, hi = step.marks.get("lo"), step.marks.get("hi")
        if lo is not None and hi is not None:
            left = s(ARRAY_LEFT + lo * CELL_W)
            right = s(ARRAY_LEFT + (hi + 1) * CELL_W)
            y = s(BRACKET_Y)
            canvas.create_line(left, y, right, y, fill=CURSOR_EDGE, width=3)
            canvas.create_line(left, y, left, y + s(12), fill=CURSOR_EDGE, width=3)
            canvas.create_line(right, y, right, y + s(12), fill=CURSOR_EDGE, width=3)
            canvas.create_text((left + right) / 2, y - s(12),
                               text=f"live window  lo={lo}  hi={hi}",
                               font=font(11, "bold"), fill=CURSOR_EDGE)

        for index, item in enumerate(order):
            x = s(item.pos)
            fill, edge, text_color = style_for(index, step)
            canvas.create_rectangle(x - cell_w / 2, s(ARRAY_Y) - cell_h / 2,
                                    x + cell_w / 2, s(ARRAY_Y) + cell_h / 2,
                                    fill=fill, outline=edge, width=2)
            canvas.create_text(x, s(ARRAY_Y), text=str(item.value),
                               font=font(15, "bold"), fill=text_color)

        for index in range(n):
            x = s(array_position(index))
            canvas.create_text(x, s(INDEX_Y), text=str(index),
                               font=mono(10), fill=MUTED)

        store = step.marks.get("store")
        if store is not None and store <= n:
            x = s(ARRAY_LEFT + store * CELL_W)
            canvas.create_line(x, s(ARRAY_Y) - cell_h / 2 - s(6),
                               x, s(ARRAY_Y) + cell_h / 2 + s(6),
                               fill=LESS_EDGE, width=3)
            canvas.create_text(x, s(ARRAY_Y) + cell_h / 2 + s(16), text="store",
                               font=font(9, "bold"), fill=LESS_EDGE)

        target = step.marks.get("target")
        if target is not None:
            x = s(array_position(target))
            canvas.create_text(x, s(TARGET_Y), text="▲",
                               font=font(13, "bold"), fill=TARGET_MARK)
            canvas.create_text(x, s(TARGET_Y + 16),
                               text=f"target {target}",
                               font=font(10, "bold"), fill=TARGET_MARK)

        draw_rounds(step, n)
        draw_code(step)
        draw_panel(step)
        draw_legend()

        if attempt < 3:
            bounds = canvas.bbox("all")
            width, height = canvas.winfo_width(), canvas.winfo_height()
            if bounds and width > 1 and height > 1:
                overflow = max((bounds[2] + 4) / width, (bounds[3] + 4) / height)
                if overflow > 1.0:
                    state["scale"] /= overflow
                    draw(step, attempt + 1)

    def draw_rounds(step: Step, n: int) -> None:
        canvas.create_text(s(ROUNDS_LEFT), s(ROUNDS_TOP - 14), anchor="w",
                           text="work per round — each bar is the window that "
                                "round had to scan:",
                           font=font(11, "italic"), fill=MUTED)
        widest = s(ROUNDS_RIGHT - ROUNDS_LEFT - 120)
        y = s(ROUNDS_TOP + 10)
        shown = step.rounds or []
        for number, size in shown:
            width = widest * (size / n)
            canvas.create_rectangle(s(ROUNDS_LEFT), y, s(ROUNDS_LEFT) + width,
                                    y + s(ROUNDS_BAR_H), fill=BAR_FILL,
                                    outline=BAR_EDGE)
            canvas.create_text(s(ROUNDS_LEFT) + width + s(8),
                               y + s(ROUNDS_BAR_H) / 2, anchor="w",
                               text=f"round {number}: {size} elements",
                               font=font(10), fill=TEXT)
            y += s(ROUNDS_BAR_H + 8)
        if shown:
            total = sum(size for _, size in shown)
            canvas.create_text(s(ROUNDS_LEFT), y + s(6), anchor="nw",
                               text=f"total scanned so far: {total}"
                                    f"   (the O(n) bound is 2n = {2 * n})",
                               font=font(10, "bold"), fill=ACCENT)
        else:
            canvas.create_text(s(ROUNDS_LEFT), y, anchor="nw",
                               text="— no round finished yet —",
                               font=font(10, "italic"), fill=MUTED)

    def draw_code(step: Step) -> None:
        line_h = s(CODE_LINE_H)
        height = len(CODE) * line_h + s(20)
        canvas.create_rectangle(s(CODE_LEFT - 12), s(CODE_TOP - 26),
                                s(CODE_RIGHT), s(CODE_TOP) + height,
                                fill=CODE_BG, outline=CODE_BG)
        canvas.create_text(s(CODE_LEFT), s(CODE_TOP - 12), anchor="w",
                           text="the code", font=font(12, "bold"), fill=CODE_DIM)
        for number, line in enumerate(CODE):
            y = s(CODE_TOP + 12) + number * line_h
            active = number == step.code_line
            if active:
                canvas.create_rectangle(s(CODE_LEFT - 8), y - s(9),
                                        s(CODE_RIGHT - 4), y + s(10),
                                        fill=CODE_HL, outline=CODE_HL)
            canvas.create_text(
                s(CODE_LEFT), y, anchor="w", text=line,
                font=mono(14, "bold" if active else "normal"),
                fill=CODE_HL_FG if active else
                (CODE_DIM if line.strip().startswith("#") else CODE_FG))

    def draw_panel(step: Step) -> None:
        canvas.create_rectangle(s(PANEL_LEFT), s(PANEL_TOP), s(PANEL_RIGHT),
                                s(CANVAS_H - 16), fill=PANEL_BG,
                                outline=PANEL_EDGE)
        wrap = s(PANEL_RIGHT - PANEL_LEFT - 32)
        canvas.create_text(s(PANEL_LEFT + 16), s(PANEL_TOP + 22), anchor="w",
                           text=step.title, font=font(14, "bold"), fill=TEXT,
                           width=wrap)
        y = s(PANEL_TOP + 52)
        for line in step.detail:
            drawn = canvas.create_text(s(PANEL_LEFT + 16), y, anchor="nw",
                                       text="• " + line, font=font(11),
                                       fill=TEXT, width=wrap)
            y = canvas.bbox(drawn)[3] + s(8)

    def draw_legend() -> None:
        entries = [
            (PIVOT_FILL, PIVOT_EDGE, "pivot"),
            (CURSOR_FILL, CURSOR_EDGE, "scan pointer i"),
            (LESS_FILL, LESS_EDGE, "proven < pivot"),
            (DISCARD_FILL, DISCARD_EDGE, "discarded"),
            (FOUND_FILL, FOUND_EDGE, "the answer"),
        ]
        x = s(CODE_LEFT - 12)
        y = s(CANVAS_H - 148)
        canvas.create_text(x, y - s(22), anchor="w", text="legend",
                           font=font(11, "bold"), fill=MUTED)
        for fill, edge, label in entries:
            canvas.create_rectangle(x, y - s(8), x + s(18), y + s(8),
                                    fill=fill, outline=edge, width=2)
            canvas.create_text(x + s(26), y, anchor="w", text=label,
                               font=font(10), fill=TEXT)
            y += s(24)

    def redraw() -> None:
        if state["steps"]:
            draw(state["steps"][state["index"]])

    def on_resize(event) -> None:
        if event.width < 50 or event.height < 50:
            return
        new_scale = min(event.width / CANVAS_W, event.height / CANVAS_H)
        if abs(new_scale - state["scale"]) < 0.005:
            return
        state["scale"] = new_scale
        redraw()

    canvas.bind("<Configure>", on_resize)

    # --- stepping ---------------------------------------------------------

    def show(index: int, animate: bool = True) -> None:
        state["index"] = max(0, min(index, len(state["steps"]) - 1))
        step = state["steps"][state["index"]]
        layout(step.order)
        if animate:
            state["animating"] = True
            tween(step, 0)
        else:
            snap(step.order)
            draw(step)
        update_buttons()

    def tween(step: Step, frame: int) -> None:
        if frame > ANIM_FRAMES:
            for item in step.order:
                item.pos = item.target
            draw(step)
            state["animating"] = False
            if state["playing"]:
                root.after(AUTOPLAY_MS, auto_advance)
            return
        t = frame / ANIM_FRAMES
        eased = t * t * (3 - 2 * t)
        for item in step.order:
            item.pos += (item.target - item.pos) * eased * 0.6
        draw(step)
        root.after(ANIM_INTERVAL_MS, lambda: tween(step, frame + 1))

    def auto_advance() -> None:
        if not state["playing"]:
            return
        if state["index"] >= len(state["steps"]) - 1:
            set_playing(False)
            return
        show(state["index"] + 1)

    def step_forward() -> None:
        if not state["animating"]:
            show(state["index"] + 1)

    def step_back() -> None:
        if not state["animating"]:
            set_playing(False)
            show(state["index"] - 1)

    def set_playing(value: bool) -> None:
        state["playing"] = value
        play_button.config(text="Pause" if value else "Play")
        if value and not state["animating"]:
            auto_advance()

    def toggle_play() -> None:
        set_playing(not state["playing"])

    def reset(new_values: bool = False) -> None:
        set_playing(False)
        if new_values:
            size = random.randint(8, MAX_ITEMS)
            state["values"] = random.sample(range(1, 99), size)
            state["k"] = random.randint(1, size)
            state["seed"] = random.randint(0, 10_000)
        state["k"] = min(state["k"], len(state["values"]))
        state["steps"] = build_steps(state["values"], state["k"], state["seed"])
        state["index"] = 0
        snap(state["steps"][0].order)
        show(0, animate=False)

    def update_buttons() -> None:
        back_button.config(state="normal" if state["index"] > 0 else "disabled")
        last = state["index"] >= len(state["steps"]) - 1
        next_button.config(state="disabled" if last else "normal")

    # --- controls ---------------------------------------------------------

    bar = tk.Frame(root, bg=BG)
    bar.grid(row=1, column=0, pady=(0, 10))

    back_button = tk.Button(bar, text="◀ Back", command=step_back, width=10)
    back_button.pack(side="left", padx=3)
    next_button = tk.Button(bar, text="Next ▶", command=step_forward, width=10)
    next_button.pack(side="left", padx=3)
    play_button = tk.Button(bar, text="Play", command=toggle_play, width=10)
    play_button.pack(side="left", padx=3)
    tk.Button(bar, text="Restart", command=lambda: reset(False), width=10).pack(
        side="left", padx=3)
    tk.Button(bar, text="New array", command=lambda: reset(True), width=10).pack(
        side="left", padx=3)
    tk.Label(bar, text="   Right/Left arrows step · Space plays · resize to zoom",
             bg=BG, fg=MUTED).pack(side="left", padx=8)

    root.bind("<Right>", lambda _event: step_forward())
    root.bind("<Left>", lambda _event: step_back())
    root.bind("<space>", lambda _event: toggle_play())

    reset(False)
    root.update_idletasks()
    width, height = root.winfo_reqwidth(), root.winfo_reqheight()
    x = max(0, (root.winfo_screenwidth() - width) // 2)
    y = max(0, (root.winfo_screenheight() - height) // 3)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(640, 420)
    root.mainloop()


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------


def run_selftest() -> None:
    # the recorded run must land on the true kth largest, every time
    rng = random.Random(12345)
    for _ in range(400):
        size = rng.randint(1, MAX_ITEMS)
        values = [rng.randint(-50, 50) for _ in range(size)]
        k = rng.randint(1, size)
        steps = build_steps(values, k, seed=rng.randint(0, 9999))
        final = steps[-1]
        answer = final.order[final.marks["answer"]].value
        assert answer == sorted(values, reverse=True)[k - 1], (values, k, answer)
        # the multiset is only ever permuted, never altered
        assert sorted(item.value for item in final.order) == sorted(values)

    # a fixed case, checked step by step for renderability
    steps = build_steps([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, seed=7)
    assert steps
    previous = {"comparisons": 0, "swaps": 0, "scanned": 0, "rounds": 0}
    for step in steps:
        assert 0 <= step.code_line < len(CODE), step.code_line
        assert step.title and step.detail, step.title
        assert all(0 <= i < 9 for i in step.roles), step.roles
        for key in ("lo", "hi", "target", "store", "pivot", "answer"):
            if key in step.marks:
                assert 0 <= step.marks[key] <= 9, (key, step.marks[key])
        for key in previous:
            assert step.stats[key] >= previous[key], key
        previous = step.stats
        assert len(step.order) == 9

    # target index arithmetic: k=1 is the last index, k=n is index 0
    for size in (1, 5, 12):
        values = list(range(size))
        assert build_steps(values, 1, seed=1)[0].marks["target"] == size - 1
        assert build_steps(values, size, seed=1)[0].marks["target"] == 0

    # total scanned stays inside the 2n bound that makes this O(n)
    for _ in range(50):
        size = rng.randint(4, MAX_ITEMS)
        values = rng.sample(range(1, 99), size)
        k = rng.randint(1, size)
        steps = build_steps(values, k, seed=rng.randint(0, 9999))
        rounds = steps[-1].rounds
        assert sum(size_ for _, size_ in rounds) <= 2 * size, (values, k, rounds)

    # k out of range is rejected, not silently wrong
    for bad_k in (0, 4):
        try:
            build_steps([1, 2, 3], bad_k)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for k={bad_k}")

    print("ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quickselect, step by step.")
    parser.add_argument("--selftest", action="store_true",
                        help="verify the step model without opening a window")
    if parser.parse_args().selftest:
        run_selftest()
    else:
        launch()
