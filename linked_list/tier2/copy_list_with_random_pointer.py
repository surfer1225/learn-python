"""Copy List with Random Pointer
https://leetcode.com/problems/copy-list-with-random-pointer/

Tier 2 — good to prepare · Linked List

Each node has a `next` and a `random` pointer. Build a deep copy: brand new
nodes, with the same value and the same internal wiring.

Two passes with a dict is the clean answer; O(1) space via node interleaving is
the follow-up.

Example:
    Input:  [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]   # (value, random index)
    Output: an identical structure made of new nodes

Run: python linked_list/tier2/copy_list_with_random_pointer.py
"""


class Node:
    def __init__(self, x: int, next=None, random=None):
        self.val = x
        self.next = next
        self.random = random


def build_random_list(pairs: list[tuple[int, int | None]]) -> Node | None:
    """Build a list from (value, random-index) pairs; `None` means no random."""
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, rand) in enumerate(pairs):
        nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
        nodes[i].random = nodes[rand] if rand is not None else None
    return nodes[0] if nodes else None


def to_pairs(head: Node | None) -> list[tuple[int, int | None]]:
    """Flatten back into (value, random-index) pairs."""
    nodes, cur = [], head
    while cur:
        nodes.append(cur)
        cur = cur.next
    position = {id(node): i for i, node in enumerate(nodes)}
    return [(node.val, position.get(id(node.random))) for node in nodes]


def copy_random_list(head: Node | None) -> Node | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    pairs = [(7, None), (13, 0), (11, 4), (10, 2), (1, 0)]
    head = build_random_list(pairs)
    copied = copy_random_list(head)
    assert to_pairs(copied) == pairs
    assert copied is not head  # must be new nodes, not the original list
    assert copy_random_list(None) is None
    print("ok")
