"""Animated doubly linked list (the data structure behind an LRU cache).

Run it:
    python experiments/doubly_linked_list_animation.py

What you'll see: a doubly linked list drawn with two sentinels (HEAD and TAIL)
and real nodes in between. The top arrows are `next` pointers, the bottom arrows
are `prev` pointers. Each button performs one operation and animates the nodes
sliding to their new positions while the status line explains the pointer surgery
and its time complexity.

Why sentinels? A dummy HEAD and TAIL node mean insertion/removal never has to
special-case "the list is empty" or "this is the first/last node" — every real
node always has a non-null neighbour on both sides. This is exactly how an LRU
cache keeps `add`, `evict`, and `touch` at O(1).

Time complexity (see the panel in the window too):
    add at head / tail ......... O(1)   fixed number of pointer rewires
    remove head / tail ......... O(1)   unlink via known neighbours
    move a known node to front .. O(1)   unlink + relink, no scanning
    search by value ............ O(n)   must walk the chain
    access by index ............ O(n)   no random access in a linked list
"""

from __future__ import annotations

import random
import tkinter as tk

# --- appearance -------------------------------------------------------------
CANVAS_W, CANVAS_H = 1120, 460
ROW_Y = 210               # vertical center of the node row
NODE_W, NODE_H = 96, 60
STEP = 132                # horizontal distance between node centers
HEAD_X = 70
MAX_NODES = 7             # keep it readable

NODE_FILL = "#dbeafe"
NODE_EDGE = "#1d4ed8"
NODE_HOT = "#fde68a"      # highlight for the node an operation touches
SENTINEL_FILL = "#e5e7eb"
SENTINEL_EDGE = "#6b7280"
NEXT_COLOR = "#1d4ed8"    # top arrows (next)
PREV_COLOR = "#b45309"    # bottom arrows (prev)

ANIM_FRAMES = 18
ANIM_INTERVAL_MS = 16


class Node:
    """A list node. Model fields (value/prev/next) plus view fields (x/tx...).

    In production these two concerns would live in separate objects; here they
    share a class to keep the single-file animation easy to follow.
    """

    def __init__(self, value: int, label: str | None = None):
        self.value = value
        self.label = label if label is not None else str(value)
        self.prev: Node | None = None
        self.next: Node | None = None
        self.is_sentinel = label is not None
        # view state
        self.x = HEAD_X
        self.y = ROW_Y
        self.tx = HEAD_X   # target x
        self.ty = ROW_Y    # target y


class DoublyLinkedList:
    """Classic sentinel-bounded doubly linked list. Every op below is O(1)."""

    def __init__(self):
        self.head = Node(0, label="HEAD")   # dummy
        self.tail = Node(0, label="TAIL")   # dummy
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_between(self, node: Node, left: Node, right: Node) -> None:
        # Four pointer writes — independent of list length -> O(1).
        node.prev, node.next = left, right
        left.next = node
        right.prev = node
        self.size += 1

    def _unlink(self, node: Node) -> None:
        # Two pointer writes to bypass `node` -> O(1).
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def add_front(self, node: Node) -> None:
        self._insert_between(node, self.head, self.head.next)

    def add_back(self, node: Node) -> None:
        self._insert_between(node, self.tail.prev, self.tail)

    def remove(self, node: Node) -> None:
        self._unlink(node)

    def move_to_front(self, node: Node) -> None:
        self._unlink(node)
        self._insert_between(node, self.head, self.head.next)

    def real_nodes(self) -> list[Node]:
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur)
            cur = cur.next
        return out


def _ease_out(t: float) -> float:
    """Cubic ease-out so motion decelerates into place."""
    return 1 - (1 - t) ** 3


class DLLVisualizer:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Doubly Linked List — animated")
        root.resizable(False, False)

        self.dll = DoublyLinkedList()
        self.leaving: list[Node] = []   # nodes sliding off-screen after removal
        self.hot: set[Node] = set()     # nodes to highlight this operation
        self.animating = False
        self._counter = 0               # for auto-incrementing node values

        self.canvas = tk.Canvas(root, width=CANVAS_W, height=CANVAS_H, bg="white", highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, font=("Helvetica", 13), pady=6, justify="left")
        self.status.pack(fill="x")

        self._build_buttons(root)

        for _ in range(3):              # start with a few nodes
            self._do(lambda n: self.dll.add_back(n), "Initial fill", silent=True)
        self._snap_positions()
        self._render()
        self._set_status("Ready. Every end-operation here is O(1) — watch the node count, the work stays constant.")

    # -- UI -----------------------------------------------------------------
    def _build_buttons(self, root: tk.Tk) -> None:
        bar = tk.Frame(root)
        bar.pack(pady=8)
        buttons = [
            ("Add Front (MRU)", self.add_front),
            ("Add Back", self.add_back),
            ("Remove Front", self.remove_front),
            ("Remove Back (evict LRU)", self.remove_back),
            ("Touch Random (get)", self.touch_random),
            ("Reset", self.reset),
        ]
        for text, cmd in buttons:
            tk.Button(bar, text=text, command=cmd).pack(side="left", padx=4)

    def _set_status(self, text: str) -> None:
        self.status.config(text=text)

    # -- operations (each explains its O(1) pointer surgery) ----------------
    def add_front(self) -> None:
        if self._full():
            return
        node = self._new_node()
        self.dll.add_front(node)
        self.hot = {node}
        self._commit(
            f"add_front(value={node.value}): rewire HEAD.next, new.prev, new.next, "
            f"old-first.prev = 4 pointer writes -> O(1)."
        )

    def add_back(self) -> None:
        if self._full():
            return
        node = self._new_node()
        self.dll.add_back(node)
        self.hot = {node}
        self._commit(
            f"add_back(value={node.value}): symmetric to add_front, 4 pointer writes -> O(1)."
        )

    def remove_front(self) -> None:
        first = self.dll.head.next
        if first is self.dll.tail:
            self._set_status("List is empty — nothing to remove.")
            return
        self.dll.remove(first)
        self._start_leaving(first)
        self._commit(
            f"remove_front(value={first.value}): 2 pointer writes bypass the node -> O(1)."
        )

    def remove_back(self) -> None:
        last = self.dll.tail.prev
        if last is self.dll.head:
            self._set_status("List is empty — nothing to remove.")
            return
        self.dll.remove(last)
        self._start_leaving(last)
        self._commit(
            f"remove_back(value={last.value}): this is exactly LRU eviction — "
            f"unlink the tail-most node, 2 writes -> O(1)."
        )

    def touch_random(self) -> None:
        nodes = self.dll.real_nodes()
        if not nodes:
            self._set_status("List is empty — nothing to touch.")
            return
        node = random.choice(nodes)
        self.dll.move_to_front(node)
        self.hot = {node}
        self._commit(
            f"touch(value={node.value}): unlink (2 writes) then insert at front (4 writes). "
            f"We already hold the node reference, so NO search -> O(1)."
        )

    def reset(self) -> None:
        if self.animating:
            return
        self.dll = DoublyLinkedList()
        self.leaving.clear()
        self.hot.clear()
        self._counter = 0
        for _ in range(3):
            self._do(lambda n: self.dll.add_back(n), "", silent=True)
        self._snap_positions()
        self._render()
        self._set_status("Reset. Try the operations and watch the pointer counts stay constant.")

    # -- helpers ------------------------------------------------------------
    def _full(self) -> bool:
        if self.dll.size >= MAX_NODES:
            self._set_status(f"Capacity {MAX_NODES} reached (kept small for readability) — remove a node first.")
            return True
        return False

    def _new_node(self) -> Node:
        self._counter += 1
        return Node(self._counter)

    def _do(self, op, _msg, silent=False) -> None:
        op(self._new_node())

    def _start_leaving(self, node: Node) -> None:
        node.ty = -NODE_H          # slide up and out
        self.leaving.append(node)
        self.hot = {node}

    def _commit(self, status: str) -> None:
        """Lay out targets and animate everything into place."""
        if self.animating:
            return
        self._set_status(status)
        self._layout_targets()
        self._animate()

    def _layout_targets(self) -> None:
        nodes = self.dll.real_nodes()
        # sentinels
        self.dll.head.tx = HEAD_X
        self.dll.head.ty = ROW_Y
        self.dll.tail.tx = HEAD_X + (len(nodes) + 1) * STEP
        self.dll.tail.ty = ROW_Y
        for i, n in enumerate(nodes):
            n.tx = HEAD_X + (i + 1) * STEP
            n.ty = ROW_Y

    def _snap_positions(self) -> None:
        """Place everything at its target immediately (no animation)."""
        self._layout_targets()
        for n in self._all_drawables():
            n.x, n.y = n.tx, n.ty

    def _all_drawables(self) -> list[Node]:
        return [self.dll.head, *self.dll.real_nodes(), self.dll.tail]

    # -- animation loop -----------------------------------------------------
    def _animate(self) -> None:
        self.animating = True
        movers = self._all_drawables() + self.leaving
        starts = {id(n): (n.x, n.y) for n in movers}
        self._step(movers, starts, frame=0)

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
            self.leaving.clear()          # off-screen nodes are gone
            self.animating = False

    # -- drawing ------------------------------------------------------------
    def _render(self) -> None:
        self.canvas.delete("all")
        self._draw_complexity_panel()

        chain = self._all_drawables()
        for a, b in zip(chain, chain[1:]):          # arrows between neighbours
            self._draw_next_arrow(a, b)
            self._draw_prev_arrow(b, a)
        for n in chain + self.leaving:              # boxes on top of arrows
            self._draw_node(n)

    def _draw_node(self, n: Node) -> None:
        if n.is_sentinel:
            fill, edge = SENTINEL_FILL, SENTINEL_EDGE
        else:
            fill = NODE_HOT if n in self.hot else NODE_FILL
            edge = NODE_EDGE
        x, y = n.x, n.y
        self.canvas.create_rectangle(
            x - NODE_W / 2, y - NODE_H / 2, x + NODE_W / 2, y + NODE_H / 2,
            fill=fill, outline=edge, width=2,
        )
        self.canvas.create_text(x, y, text=n.label, font=("Helvetica", 16, "bold"))

    def _draw_next_arrow(self, a: Node, b: Node) -> None:
        # top arrow, points a -> b (next)
        y = min(a.y, b.y) - NODE_H / 2 - 10
        self.canvas.create_line(
            a.x + NODE_W / 4, y, b.x - NODE_W / 4, y,
            fill=NEXT_COLOR, width=2, arrow="last", smooth=True,
        )

    def _draw_prev_arrow(self, a: Node, b: Node) -> None:
        # bottom arrow, points a -> b (prev, i.e. right node back to left node)
        y = max(a.y, b.y) + NODE_H / 2 + 10
        self.canvas.create_line(
            a.x - NODE_W / 4, y, b.x + NODE_W / 4, y,
            fill=PREV_COLOR, width=2, arrow="last", smooth=True,
        )

    def _draw_complexity_panel(self) -> None:
        lines = [
            "next  →  (top, blue)      prev  →  (bottom, orange)",
            "",
            "add head/tail .......... O(1)",
            "remove head/tail ....... O(1)",
            "move known node front .. O(1)",
            "search by value ........ O(n)",
            "access by index ........ O(n)",
        ]
        x, y = 20, 20
        self.canvas.create_rectangle(x - 10, y - 10, x + 300, y + 150, fill="#f9fafb", outline="#d1d5db")
        for i, line in enumerate(lines):
            self.canvas.create_text(
                x, y + i * 20, text=line, anchor="w",
                font=("Menlo", 11), fill="#374151",
            )


def run() -> None:
    root = tk.Tk()
    DLLVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    run()
