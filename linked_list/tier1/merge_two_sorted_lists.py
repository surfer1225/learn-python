"""Merge Two Sorted Lists
https://leetcode.com/problems/merge-two-sorted-lists/

Tier 1 — must prepare · Linked List

Merge two sorted linked lists into one sorted list by splicing nodes together.

Example:
    Input:  1 -> 2 -> 4  and  1 -> 3 -> 4
    Output: 1 -> 1 -> 2 -> 3 -> 4 -> 4

Run: python linked_list/tier1/merge_two_sorted_lists.py
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


def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    merged = merge_two_lists(build_list([1, 2, 4]), build_list([1, 3, 4]))
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(build_list([]), build_list([0]))) == [0]
    assert to_list(merge_two_lists(build_list([]), build_list([]))) == []
    print("ok")
