"""Invert Binary Tree
https://leetcode.com/problems/invert-binary-tree/

Tier 1 — must prepare · Trees

Invert a binary tree: swap every node's left and right child.

Example:
    Input:  [4, 2, 7, 1, 3, 6, 9]
    Output: [4, 7, 2, 9, 6, 3, 1]

Run: python trees/tier1/invert_binary_tree.py
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


def invert_tree(root: TreeNode | None) -> TreeNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert to_level_order(invert_tree(build_tree([4, 2, 7, 1, 3, 6, 9]))) == [
        4, 7, 2, 9, 6, 3, 1,
    ]
    assert to_level_order(invert_tree(build_tree([2, 1, 3]))) == [2, 3, 1]
    assert invert_tree(None) is None
    print("ok")
