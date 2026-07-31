"""Merge k Sorted Lists
https://leetcode.com/problems/merge-k-sorted-lists/

Tier 2 — good to prepare · Linked List

Merge `k` sorted linked lists into one sorted list.

Know the complexity of both the heap and the divide-and-conquer approaches, and
why merging one-at-a-time is worse than both.

Example:
    Input:  [[1, 4, 5], [1, 3, 4], [2, 6]]
    Output: [1, 1, 2, 3, 4, 4, 5, 6]

Run: python linked_list/tier2/merge_k_sorted_lists.py
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


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
    assert to_list(merge_k_lists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert to_list(merge_k_lists([])) == []
    assert to_list(merge_k_lists([build_list([])])) == []
    print("ok")
