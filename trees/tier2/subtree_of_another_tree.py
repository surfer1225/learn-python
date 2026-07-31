"""Subtree of Another Tree
https://leetcode.com/problems/subtree-of-another-tree/

Tier 2 — good to prepare · Trees

Return `True` if `sub_root` appears as a subtree of `root` — matching a node and
all of its descendants exactly.

Example:
    Input:  root = [3, 4, 5, 1, 2], sub_root = [4, 1, 2]
    Output: True

Run: python trees/tier2/subtree_of_another_tree.py
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


def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_subtree(build_tree([3, 4, 5, 1, 2]), build_tree([4, 1, 2])) is True
    assert is_subtree(
        build_tree([3, 4, 5, 1, 2, None, None, None, None, 0]), build_tree([4, 1, 2])
    ) is False
    assert is_subtree(build_tree([1, 1]), build_tree([1])) is True
    print("ok")
