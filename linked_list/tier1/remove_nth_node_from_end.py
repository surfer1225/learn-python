"""Remove Nth Node From End of List
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

Tier 1 — must prepare · Linked List

Remove the nth node from the end of the list and return the head. One pass.

A dummy head makes the "remove the first node" case disappear.

Example:
    Input:  1 -> 2 -> 3 -> 4 -> 5, n = 2
    Output: 1 -> 2 -> 3 -> 5

Run: python linked_list/tier1/remove_nth_node_from_end.py
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


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert to_list(remove_nth_from_end(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(remove_nth_from_end(build_list([1]), 1)) == []
    assert to_list(remove_nth_from_end(build_list([1, 2]), 1)) == [1]
    print("ok")
