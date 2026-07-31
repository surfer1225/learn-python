"""Construct Binary Tree from Preorder and Inorder Traversal
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Tier 2 — good to prepare · Trees

Rebuild the tree from its preorder and inorder traversals. All values are
unique.

Preorder gives you the root; inorder tells you how the rest splits.

Example:
    Input:  preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]
    Output: [3, 9, 20, None, None, 15, 7]

Run: python trees/tier2/construct_binary_tree_from_preorder_and_inorder.py
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


def construct_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    built = construct_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    assert to_level_order(built) == [3, 9, 20, None, None, 15, 7]
    assert to_level_order(construct_tree([-1], [-1])) == [-1]
    assert construct_tree([], []) is None
    print("ok")
