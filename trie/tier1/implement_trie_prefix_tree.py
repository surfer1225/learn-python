"""Implement Trie (Prefix Tree)
https://leetcode.com/problems/implement-trie-prefix-tree/

Tier 1 — must prepare · Tries

Implement a trie supporting `insert`, `search` (exact word), and `starts_with`
(any word with that prefix).

Example:
    Input:  insert("apple"), search("apple"), search("app"), starts_with("app")
    Output: True, False, True

Run: python trie/tier1/implement_trie_prefix_tree.py
"""


class Trie:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def insert(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        """True only if the exact word was inserted."""
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        """True if any inserted word begins with `prefix`."""
        raise NotImplementedError


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    print("ok")
