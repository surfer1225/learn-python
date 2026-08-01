"""Step-through walkthrough of heapify — build a heap from an unordered array.

Run it:
    python heap/heapify_walkthrough.py              # open the walkthrough
    python heap/heapify_walkthrough.py --selftest   # verify the model, print ok

Unlike `heap_visualization.py` (a free-form heap you poke at), this file does
one thing: it explains `heapify` one step at a time. It starts PAUSED. Press
Next to advance; every step highlights the line of code being executed and
explains what it does and why.

    Next / Right arrow ...... advance one step
    Back / Left arrow ....... rewind one step
    Play / Space ............ auto-advance until paused again
    New array ............... regenerate with fresh random values

What heapify does: takes an array in ARBITRARY order and rearranges it in place
so that every parent beats its children. Same elements, new positions. The
result is a valid heap, NOT a sorted array — that distinction is the single most
common misunderstanding.

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)

Two details carry the whole algorithm, and the animation calls out both:

  * Start at n // 2 - 1, because every index from n // 2 onward is a leaf, and
    a leaf is already a valid heap of one element. Half the array is free.
  * Walk BACKWARDS, because sift_down(i) is only correct when i's two subtrees
    are already valid heaps. Right-to-left guarantees that.

Why it is O(n) and not O(n log n): sift-down cost is bounded by a node's own
HEIGHT, not the tree's. Half the nodes are leaves (height 0), a quarter have
height 1, an eighth height 2 — and n/2*0 + n/4*1 + n/8*2 + ... converges to n.
Building the same heap by pushing n items one at a time is genuinely O(n log n),
because sift-UP cost is bounded by DEPTH, and half the nodes sit at maximum
depth. Same tree, opposite direction, different complexity class.

This is a min-heap. For a max-heap, flip the comparison — or, in Python, negate
the priorities, since `heapq` has no `reverse` flag.
"""

from __future__ import annotations

import argparse
import random

# --- layout -----------------------------------------------------------------
CANVAS_W, CANVAS_H = 1280, 786

TREE_TOP = 118
LEVEL_H = 86
TREE_LEFT, TREE_RIGHT = 44, 872
NODE_R = 25

ARRAY_Y = 452
CELL_W, CELL_H = 58, 44
ARRAY_LEFT = 60

CODE_LEFT = 906
CODE_TOP = 96
CODE_LINE_H = 21
CODE_RIGHT = 1258

PANEL_TOP = 528
PANEL_LEFT = 40
PANEL_RIGHT = 872

MAX_ITEMS = 15

# --- colors -----------------------------------------------------------------
BG = "#f8fafc"
NODE_FILL = "#ffffff"
NODE_EDGE = "#94a3b8"
LEAF_FILL = "#f1f5f9"
LEAF_EDGE = "#cbd5e1"
DONE_FILL = "#dcfce7"     # subtree already known to be a valid heap
DONE_EDGE = "#16a34a"
CURSOR_FILL = "#bfdbfe"   # the node currently being sifted down
CURSOR_EDGE = "#1d4ed8"
CHILD_FILL = "#fde68a"    # children under comparison
SWAP_FILL = "#fecaca"     # the pair about to trade places
EDGE_COLOR = "#cbd5e1"
EDGE_ACTIVE = "#1d4ed8"
CELL_EDGE = "#cbd5e1"
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

ANIM_FRAMES = 14
ANIM_INTERVAL_MS = 16
AUTOPLAY_MS = 1100

# The code shown in the side panel. Steps point at a line by index.
CODE = [
    "def heapify(a):",
    "    n = len(a)",
    "    # every index >= n//2 is a leaf",
    "    for i in range(n // 2 - 1, -1, -1):",
    "        sift_down(a, i, n)",
    "",
    "def sift_down(a, i, n):",
    "    while True:",
    "        left, right = 2*i + 1, 2*i + 2",
    "        best = i",
    "        if left  < n and a[left]  < a[best]:",
    "            best = left",
    "        if right < n and a[right] < a[best]:",
    "            best = right",
    "        if best == i:",
    "            return   # subtree is a valid heap",
    "        a[i], a[best] = a[best], a[i]",
    "        i = best",
]


class Item:
    """One array entry. Stable identity so the view can tween it between steps."""

    def __init__(self, value: int):
        self.value = value
        self.pos = [0.0, 0.0, 0.0]     # current  [tree_x, tree_y, array_x]
        self.target = [0.0, 0.0, 0.0]  # where this step wants it

    def __repr__(self) -> str:
        return f"Item({self.value})"


class Step:
    """One paused frame: an ordering, a code line, and the narration for it."""

    def __init__(self, order, code_line, title, detail, roles, stats):
        self.order = list(order)
        self.code_line = code_line
        self.title = title
        self.detail = detail
        self.roles = dict(roles)   # index -> "cursor" | "child" | "swap" | "done"
        self.stats = dict(stats)   # comparisons / swaps counted so far


def tree_position(index: int) -> tuple[float, float]:
    """Tree coordinates for an array index, from the completeness property."""
    depth = 0
    while (1 << (depth + 1)) - 1 <= index:
        depth += 1
    slot = index - ((1 << depth) - 1)
    span = (TREE_RIGHT - TREE_LEFT) / (1 << depth)
    return TREE_LEFT + span * (slot + 0.5), TREE_TOP + depth * LEVEL_H


def array_position(index: int) -> float:
    return ARRAY_LEFT + index * CELL_W + CELL_W / 2


def height_of(index: int, n: int) -> int:
    """Height of the subtree rooted at `index` — the real cost bound."""
    left, right = 2 * index + 1, 2 * index + 2
    if left >= n:
        return 0
    best = height_of(left, n)
    if right < n:
        best = max(best, height_of(right, n))
    return best + 1


def build_steps(values: list[int]) -> list[Step]:
    """Run heapify on `values`, recording a narrated Step at every decision."""
    items = [Item(v) for v in values[:MAX_ITEMS]]
    n = len(items)
    steps: list[Step] = []
    stats = {"comparisons": 0, "swaps": 0}

    def add(code_line, title, detail, roles=None):
        steps.append(Step(items, code_line, title, detail, roles or {}, stats))

    def done_roles(upto: int) -> dict[int, str]:
        """Indices >= upto are roots of subtrees already proven valid."""
        return {index: "done" for index in range(upto, n)}

    first_leaf = n // 2
    add(
        1,
        "Start: an array in arbitrary order",
        [
            f"{n} values, no ordering assumed. A heap only requires that each "
            "parent beats its children — siblings are unrelated, and the array "
            "will NOT come out sorted.",
            "The tree above and the array below are the same thing: index "
            "arithmetic gives the shape, so no pointers exist.",
        ],
    )
    add(
        2,
        f"Indices {first_leaf}..{n - 1} are leaves — already done",
        [
            f"Any index >= n // 2 = {first_leaf} has no children (2i+1 would be "
            f"past the end). A childless node is a valid heap of size one.",
            "That is half the array handled before doing any work at all, and it "
            "is the first half of why heapify beats n log n.",
        ],
        done_roles(first_leaf),
    )
    add(
        3,
        f"Loop backwards from i = n // 2 - 1 = {first_leaf - 1}",
        [
            "Walking right-to-left matters: sift_down(i) is only correct if i's "
            "two subtrees are ALREADY valid heaps.",
            "Going backwards guarantees that — by the time we reach a node, "
            "everything beneath it is finished.",
        ],
        done_roles(first_leaf),
    )

    for start in range(n // 2 - 1, -1, -1):
        settled = done_roles(start + 1)
        add(
            4,
            f"i = {start}: sift down the subtree rooted here",
            [
                f"Value {items[start].value}, subtree height "
                f"{height_of(start, n)}. Both of its subtrees are already valid "
                "heaps (green), so a single sift-down fixes this one.",
                "Work is bounded by this node's HEIGHT, not the tree's — that is "
                "the whole O(n) argument.",
            ],
            {**settled, start: "cursor"},
        )
        i = start
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            children = [c for c in (left, right) if c < n]
            if not children:
                add(
                    7,
                    f"Index {i} is a leaf — stop",
                    [
                        "No children, so 2i+1 is past the end of the array. "
                        "Nothing can sink further.",
                    ],
                    {**settled, i: "cursor"},
                )
                break

            shown = ", ".join(f"a[{c}] = {items[c].value}" for c in children)
            add(
                8,
                f"Children of {i}: {'left ' + str(left) if left < n else ''}"
                f"{', right ' + str(right) if right < n else ''}",
                [
                    f"left = 2*{i}+1 = {left}"
                    + (f", right = 2*{i}+2 = {right}" if right < n else
                       f" (right = {right} is past the end)"),
                    f"Comparing a[{i}] = {items[i].value} against {shown}.",
                ],
                {**settled, i: "cursor", **{c: "child" for c in children}},
            )

            best = i
            for child in children:
                stats["comparisons"] += 1
                if items[child].value < items[best].value:
                    best = child
            add(
                10 if len(children) == 1 else 12,
                f"Best of the three is index {best} ({items[best].value})",
                [
                    "Pick the smaller CHILD, not just any child that beats the "
                    "parent. Swapping with the larger one would leave it above "
                    "its own sibling and break the other subtree.",
                    f"Comparisons so far: {stats['comparisons']}.",
                ],
                {**settled, i: "cursor", **{c: "child" for c in children}},
            )

            if best == i:
                add(
                    14,
                    "Parent already wins — subtree is a valid heap",
                    [
                        f"a[{i}] = {items[i].value} beats both children, so the "
                        "invariant holds here and everything below is untouched.",
                        "Return to the outer loop.",
                    ],
                    {**settled, i: "done"},
                )
                break

            add(
                16,
                f"Swap index {i} ({items[i].value}) with {best} ({items[best].value})",
                [
                    f"{items[best].value} belongs above {items[i].value}. After "
                    "the swap the parent is correct, but the child we just "
                    "demoted may now violate the invariant further down.",
                    f"Swaps so far: {stats['swaps'] + 1}.",
                ],
                {**settled, i: "swap", best: "swap"},
            )
            items[i], items[best] = items[best], items[i]
            stats["swaps"] += 1
            i = best
            add(
                17,
                f"Descend: i = {i}",
                [
                    "Follow the demoted value down and repeat. Each iteration "
                    "drops exactly one level, so a sift-down costs at most the "
                    "node's height.",
                ],
                {**settled, i: "cursor"},
            )

    order = [item.value for item in items]
    sorted_order = sorted(order)
    add(
        0,
        "Done — valid heap, and note it is NOT sorted",
        [
            f"Result: {order}",
            f"Sorted would be: {sorted_order}   <- different, and that is correct.",
            f"Root a[0] = {order[0]} is the minimum. Only parent-beats-children "
            "is guaranteed; siblings are unordered.",
            f"Total: {stats['comparisons']} comparisons, {stats['swaps']} swaps "
            f"for n = {n}. Pushing one at a time would cost O(n log n); this is "
            "O(n), because cost is bounded by height and half the nodes are "
            "leaves of height 0.",
        ],
        done_roles(0),
    )
    return steps


# --------------------------------------------------------------------------
# View
# --------------------------------------------------------------------------


def launch(values: list[int] | None = None) -> None:
    import tkinter as tk

    state = {
        "values": values or random.sample(range(1, 99), 10),
        "steps": [],
        "index": 0,
        "playing": False,
        "animating": False,
    }

    root = tk.Tk()
    root.title("Heapify — step by step")
    root.configure(bg=BG)
    root.lift()
    root.attributes("-topmost", True)
    root.after(400, lambda: root.attributes("-topmost", False))

    canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg=BG,
                       highlightthickness=0)
    canvas.grid(row=0, column=0, padx=10, pady=(10, 4))

    # --- geometry ---------------------------------------------------------

    def layout(order: list[Item]) -> None:
        for index, item in enumerate(order):
            tx, ty = tree_position(index)
            item.target = [tx, ty, array_position(index)]

    def snap(order: list[Item]) -> None:
        layout(order)
        for item in order:
            item.pos = list(item.target)

    # --- drawing ----------------------------------------------------------

    def style_for(index: int, step: Step) -> tuple[str, str]:
        role = step.roles.get(index)
        if role == "swap":
            return SWAP_FILL, CURSOR_EDGE
        if role == "cursor":
            return CURSOR_FILL, CURSOR_EDGE
        if role == "child":
            return CHILD_FILL, ACCENT
        if role == "done":
            return DONE_FILL, DONE_EDGE
        n = len(step.order)
        if index >= n // 2:
            return LEAF_FILL, LEAF_EDGE
        return NODE_FILL, NODE_EDGE

    def draw(step: Step) -> None:
        canvas.delete("all")
        order = step.order
        n = len(order)

        canvas.create_text(
            22, 24, anchor="w", text="heapify — build a heap from an unordered array",
            font=("Helvetica", 17, "bold"), fill=TEXT,
        )
        canvas.create_text(
            22, 48, anchor="w",
            text="parent(i) = (i-1)//2     left(i) = 2i+1     right(i) = 2i+2"
                 "     ·     O(n) total, not O(n log n)",
            font=("Courier", 11), fill=MUTED,
        )
        canvas.create_text(
            22, 70, anchor="w",
            text=f"step {state['index'] + 1} / {len(state['steps'])}"
                 f"     comparisons {step.stats['comparisons']}"
                 f"     swaps {step.stats['swaps']}",
            font=("Courier", 11, "bold"), fill=ACCENT,
        )

        for index in range(n):
            for child in (2 * index + 1, 2 * index + 2):
                if child < n:
                    active = (step.roles.get(index) in ("cursor", "swap")
                              and step.roles.get(child) in ("child", "swap"))
                    canvas.create_line(
                        order[index].pos[0], order[index].pos[1],
                        order[child].pos[0], order[child].pos[1],
                        fill=EDGE_ACTIVE if active else EDGE_COLOR,
                        width=3 if active else 2,
                    )

        for index, item in enumerate(order):
            x, y = item.pos[0], item.pos[1]
            fill, edge = style_for(index, step)
            canvas.create_oval(x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R,
                               fill=fill, outline=edge, width=2)
            canvas.create_text(x, y, text=str(item.value),
                               font=("Helvetica", 14, "bold"), fill=TEXT)
            canvas.create_text(x + NODE_R + 1, y - NODE_R + 1, text=f"[{index}]",
                               anchor="w", font=("Courier", 9), fill=MUTED)

        canvas.create_text(ARRAY_LEFT, ARRAY_Y - CELL_H, anchor="w",
                           text="the array — the heap's only real storage:",
                           font=("Helvetica", 11, "italic"), fill=MUTED)
        for index in range(n):
            left = ARRAY_LEFT + index * CELL_W
            canvas.create_rectangle(left, ARRAY_Y - CELL_H / 2,
                                    left + CELL_W, ARRAY_Y + CELL_H / 2,
                                    fill="#ffffff", outline=CELL_EDGE)
            canvas.create_text(left + CELL_W / 2, ARRAY_Y + CELL_H / 2 + 12,
                               text=str(index), font=("Courier", 10), fill=MUTED)
        for index, item in enumerate(order):
            x = item.pos[2]
            fill, edge = style_for(index, step)
            canvas.create_rectangle(x - CELL_W / 2 + 3, ARRAY_Y - CELL_H / 2 + 3,
                                    x + CELL_W / 2 - 3, ARRAY_Y + CELL_H / 2 - 3,
                                    fill=fill, outline=edge, width=2)
            canvas.create_text(x, ARRAY_Y, text=str(item.value),
                               font=("Helvetica", 13, "bold"), fill=TEXT)

        draw_code(step)
        draw_panel(step)
        draw_legend()

    def draw_code(step: Step) -> None:
        height = len(CODE) * CODE_LINE_H + 20
        canvas.create_rectangle(CODE_LEFT - 12, CODE_TOP - 26, CODE_RIGHT,
                                CODE_TOP + height, fill=CODE_BG, outline=CODE_BG)
        canvas.create_text(CODE_LEFT, CODE_TOP - 12, anchor="w", text="the code",
                           font=("Helvetica", 11, "bold"), fill=CODE_DIM)
        for number, line in enumerate(CODE):
            y = CODE_TOP + 12 + number * CODE_LINE_H
            active = number == step.code_line
            if active:
                canvas.create_rectangle(CODE_LEFT - 8, y - 9, CODE_RIGHT - 4, y + 10,
                                        fill=CODE_HL, outline=CODE_HL)
            canvas.create_text(CODE_LEFT, y, anchor="w", text=line,
                               font=("Courier", 12, "bold" if active else "normal"),
                               fill=CODE_HL_FG if active else
                               (CODE_DIM if line.strip().startswith("#") else CODE_FG))

    def draw_panel(step: Step) -> None:
        canvas.create_rectangle(PANEL_LEFT, PANEL_TOP, PANEL_RIGHT, CANVAS_H - 16,
                                fill=PANEL_BG, outline=PANEL_EDGE)
        canvas.create_text(PANEL_LEFT + 16, PANEL_TOP + 22, anchor="w",
                           text=step.title, font=("Helvetica", 14, "bold"),
                           fill=TEXT, width=PANEL_RIGHT - PANEL_LEFT - 32)
        y = PANEL_TOP + 52
        for line in step.detail:
            item = canvas.create_text(
                PANEL_LEFT + 16, y, anchor="nw", text="• " + line,
                font=("Helvetica", 11), fill=TEXT,
                width=PANEL_RIGHT - PANEL_LEFT - 32,
            )
            y = canvas.bbox(item)[3] + 8

    def draw_legend() -> None:
        entries = [
            (CURSOR_FILL, CURSOR_EDGE, "current node"),
            (CHILD_FILL, ACCENT, "children being compared"),
            (SWAP_FILL, CURSOR_EDGE, "swapping"),
            (DONE_FILL, DONE_EDGE, "valid heap"),
            (LEAF_FILL, LEAF_EDGE, "leaf (free)"),
        ]
        x = CODE_LEFT - 12
        y = CANVAS_H - 152
        canvas.create_text(x, y - 22, anchor="w", text="legend",
                           font=("Helvetica", 11, "bold"), fill=MUTED)
        for fill, edge, label in entries:
            canvas.create_rectangle(x, y - 8, x + 18, y + 8, fill=fill,
                                    outline=edge, width=2)
            canvas.create_text(x + 26, y, anchor="w", text=label,
                               font=("Helvetica", 10), fill=TEXT)
            y += 24

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
                item.pos = list(item.target)
            draw(step)
            state["animating"] = False
            if state["playing"]:
                root.after(AUTOPLAY_MS, auto_advance)
            return
        t = frame / ANIM_FRAMES
        eased = t * t * (3 - 2 * t)
        for item in step.order:
            for axis in range(3):
                start = item.pos[axis]
                item.pos[axis] = start + (item.target[axis] - start) * eased * 0.6
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
            state["values"] = random.sample(range(1, 99), random.randint(8, 12))
        state["steps"] = build_steps(state["values"])
        state["index"] = 0
        snap(state["steps"][0].order)
        show(0, animate=False)

    def update_buttons() -> None:
        back_button.config(state="normal" if state["index"] > 0 else "disabled")
        last = state["index"] >= len(state["steps"]) - 1
        next_button.config(state="disabled" if last else "normal")

    # --- controls ---------------------------------------------------------

    bar = tk.Frame(root, bg=BG)
    bar.grid(row=1, column=0, pady=(0, 12))

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
    tk.Label(bar, text="   Right/Left arrows step · Space plays", bg=BG,
             fg=MUTED).pack(side="left", padx=8)

    root.bind("<Right>", lambda _event: step_forward())
    root.bind("<Left>", lambda _event: step_back())
    root.bind("<space>", lambda _event: toggle_play())

    reset(False)
    root.mainloop()


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------


def run_selftest() -> None:
    import heapq

    for values in ([9, 4, 7, 1, 8, 2, 6, 3],
                   [5],
                   [2, 1],
                   list(range(12, 0, -1)),
                   [4, 4, 4, 4, 4]):
        steps = build_steps(values)
        assert steps, "no steps recorded"

        # the final ordering must match heapq on the same input
        final = [item.value for item in steps[-1].order]
        reference = list(values)
        heapq.heapify(reference)
        assert final == reference, (values, final, reference)

        # invariant actually holds
        for index in range(1, len(final)):
            assert final[(index - 1) // 2] <= final[index], final

        # every step is renderable: valid code line, non-empty narration,
        # in-range highlight indices, monotonic counters
        previous = {"comparisons": 0, "swaps": 0}
        for step in steps:
            assert 0 <= step.code_line < len(CODE), step.code_line
            assert step.title and step.detail, step.title
            assert all(0 <= i < len(values) for i in step.roles), step.roles
            assert step.stats["comparisons"] >= previous["comparisons"]
            assert step.stats["swaps"] >= previous["swaps"]
            previous = step.stats
            assert len(step.order) == len(values)

    # heapify never does more swaps than the O(n) bound of total node heights
    values = random.Random(0).sample(range(1, 99), 15)
    steps = build_steps(values)
    budget = sum(height_of(i, 15) for i in range(15))
    assert steps[-1].stats["swaps"] <= budget, (steps[-1].stats, budget)

    # a leaf-only array needs no work beyond the three intro steps
    assert len(build_steps([7])) == 4, len(build_steps([7]))

    # height_of matches the tree drawing: a leaf has height 0
    assert height_of(0, 1) == 0
    assert height_of(0, 3) == 1
    assert height_of(0, 7) == 2

    print("ok")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heapify, step by step.")
    parser.add_argument("--selftest", action="store_true",
                        help="verify the step model without opening a window")
    if parser.parse_args().selftest:
        run_selftest()
    else:
        launch()
