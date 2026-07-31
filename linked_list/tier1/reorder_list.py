"""Reorder List
https://leetcode.com/problems/reorder-list/

Tier 1 — must prepare · Linked List

Reorder L0 -> L1 -> ... -> Ln as L0 -> Ln -> L1 -> Ln-1 -> ... in place.

Three sub-skills in one: find the middle, reverse a half, merge alternately.

Example:
    Input:  1 -> 2 -> 3 -> 4
    Output: 1 -> 4 -> 2 -> 3

Run: python linked_list/tier1/reorder_list.py
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values: list[int]) -> ListNode | None:
    """Build a singly linked list from a Python list."""
    dummy = tail = ListNode()
    for val in values:
        tail.next = ListNode(val)
        tail = tail.next
    return dummy.next


def to_list(head: ListNode | None) -> list[int]:
    """Flatten a singly linked list back into a Python list."""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reorder_list(head: ListNode | None) -> None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    head = build_list([1, 2, 3, 4])
    reorder_list(head)
    assert to_list(head) == [1, 4, 2, 3]
    head = build_list([1, 2, 3, 4, 5])
    reorder_list(head)
    assert to_list(head) == [1, 5, 2, 4, 3]
    print("ok")
