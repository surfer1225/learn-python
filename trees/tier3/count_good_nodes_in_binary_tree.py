"""Count Good Nodes in Binary Tree
https://leetcode.com/problems/count-good-nodes-in-binary-tree/

Tier 3 — prepare if you have time · Trees

A node is good if no node on the path from the root to it has a greater value.
Return the number of good nodes.

Example:
    Input:  [3, 1, 4, 3, None, 1, 5]
    Output: 4

Run: python trees/tier3/count_good_nodes_in_binary_tree.py
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


def good_nodes(root: TreeNode | None) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert good_nodes(build_tree([3, 1, 4, 3, None, 1, 5])) == 4
    assert good_nodes(build_tree([3, 3, None, 4, 2])) == 3
    assert good_nodes(build_tree([1])) == 1
    print("ok")
