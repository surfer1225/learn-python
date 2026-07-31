"""Serialize and Deserialize Binary Tree
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Tier 3 — prepare if you have time · Trees

Design an algorithm to serialise a binary tree to a string and deserialise it
back. Any format is allowed as long as the round trip is lossless.

Example:
    Input:  [1, 2, 3, None, None, 4, 5]
    Output: the same tree, after serialize then deserialize

Run: python trees/tier3/serialize_and_deserialize_binary_tree.py
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values: list) -> TreeNode | None:
    """Build a tree from a LeetCode level-order list; `None` marks a gap."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, i = deque([root]), 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            val, i = values[i], i + 1
            if val is not None:
                node.left = TreeNode(val)
                queue.append(node.left)
        if i < len(values):
            val, i = values[i], i + 1
            if val is not None:
                node.right = TreeNode(val)
                queue.append(node.right)
    return root


def to_level_order(root: TreeNode | None) -> list:
    """Flatten a tree back into a level-order list, trimming trailing gaps."""
    if root is None:
        return []
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root: TreeNode | None, val: int) -> TreeNode | None:
    """Locate the node holding `val` (values are unique in these tests)."""
    if root is None:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def serialize(root: TreeNode | None) -> str:
    # TODO: implement
    raise NotImplementedError


def deserialize(data: str) -> TreeNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    for case in ([1, 2, 3, None, None, 4, 5], [1], [], [1, None, 2]):
        assert to_level_order(deserialize(serialize(build_tree(case)))) == case
    print("ok")
