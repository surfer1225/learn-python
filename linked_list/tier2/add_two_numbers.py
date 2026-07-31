"""Add Two Numbers
https://leetcode.com/problems/add-two-numbers/

Tier 2 — good to prepare · Linked List

Two non-empty lists hold non-negative integers with digits in reverse order.
Add them and return the sum as a list in the same form.

Example:
    Input:  [2, 4, 3] and [5, 6, 4]     # 342 + 465
    Output: [7, 0, 8]                  # 807

Run: python linked_list/tier2/add_two_numbers.py
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


def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert to_list(add_two_numbers(build_list([2, 4, 3]), build_list([5, 6, 4]))) == [7, 0, 8]
    assert to_list(add_two_numbers(build_list([0]), build_list([0]))) == [0]
    assert to_list(
        add_two_numbers(build_list([9, 9, 9, 9]), build_list([9, 9, 9, 9, 9, 9, 9]))
    ) == [8, 9, 9, 9, 0, 0, 0, 1]
    print("ok")
