"""Validate Binary Search Tree
https://leetcode.com/problems/validate-binary-search-tree/

Given the root of a binary tree, determine if it is a valid BST.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(root) is True
    print("ok")
