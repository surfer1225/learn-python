"""Min Stack
https://leetcode.com/problems/min-stack/

Tier 1 — must prepare · Stack

Design a stack supporting push, pop, top, and retrieving the minimum, each in
O(1) time.

The trick is deciding what to store alongside each value.

Example:
    Input:  push(-2), push(0), push(-3), get_min(), pop(), top(), get_min()
    Output: -3, then 0, then -2

Run: python stack/tier1/min_stack.py
"""


class MinStack:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> None:
        raise NotImplementedError

    def top(self) -> int:
        raise NotImplementedError

    def get_min(self) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)
    assert stack.get_min() == -3
    stack.pop()
    assert stack.top() == 0
    assert stack.get_min() == -2
    print("ok")
