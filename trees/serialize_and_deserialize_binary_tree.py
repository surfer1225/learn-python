"""Serialize and Deserialize Binary Tree
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Design an algorithm to serialize a binary tree to a string and deserialize it
back to the original tree.
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        # TODO: implement
        raise NotImplementedError

    def deserialize(self, data: str) -> Optional[TreeNode]:
        # TODO: implement
        raise NotImplementedError


if __name__ == "__main__":
    codec = Codec()
    root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    restored = codec.deserialize(codec.serialize(root))
    assert restored.val == 1
    print("ok")
