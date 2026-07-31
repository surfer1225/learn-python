"""Linked List Cycle
https://leetcode.com/problems/linked-list-cycle/

Tier 1 — must prepare · Linked List

Return `True` if the list contains a cycle. Use O(1) memory — Floyd's tortoise
and hare.

Example:
    Input:  3 -> 2 -> 0 -> -4, with the tail pointing back at node 2
    Output: True

Run: python linked_list/tier1/linked_list_cycle.py
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


def has_cycle(head: ListNode | None) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    head = build_list([3, 2, 0, -4])
    head.next.next.next.next = head.next  # tail loops back to the second node
    assert has_cycle(head) is True
    assert has_cycle(build_list([1, 2])) is False
    assert has_cycle(build_list([])) is False
    print("ok")
