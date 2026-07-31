"""Reverse Linked List
https://leetcode.com/problems/reverse-linked-list/

Tier 1 — must prepare · Linked List

Reverse a singly linked list and return the new head.

Be able to write it both iteratively and recursively.

Example:
    Input:  1 -> 2 -> 3 -> 4 -> 5
    Output: 5 -> 4 -> 3 -> 2 -> 1

Run: python linked_list/tier1/reverse_linked_list.py
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


def reverse_list(head: ListNode | None) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(reverse_list(build_list([1, 2]))) == [2, 1]
    assert to_list(reverse_list(build_list([]))) == []
    print("ok")
