"""Lowest Common Ancestor of a Binary Tree
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(
    root: TreeNode, p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    p = TreeNode(5)
    q = TreeNode(1)
    root = TreeNode(3, p, q)
    assert lowest_common_ancestor(root, p, q) is root
    print("ok")
