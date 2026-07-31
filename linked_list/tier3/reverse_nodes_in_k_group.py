"""Reverse Nodes in k-Group
https://leetcode.com/problems/reverse-nodes-in-k-group/

Tier 3 — prepare if you have time · Linked List

Reverse the nodes of the list `k` at a time. A trailing group of fewer than `k`
nodes stays as is. Do not modify the values, only the links.

Example:
    Input:  1 -> 2 -> 3 -> 4 -> 5, k = 2
    Output: 2 -> 1 -> 4 -> 3 -> 5

Run: python linked_list/tier3/reverse_nodes_in_k_group.py
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


def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(reverse_k_group(build_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert to_list(reverse_k_group(build_list([1]), 1)) == [1]
    print("ok")
