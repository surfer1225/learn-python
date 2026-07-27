"""Implement Trie (Prefix Tree)
https://leetcode.com/problems/implement-trie-prefix-tree/

Implement a trie with `insert`, `search`, and `startsWith` methods.
"""


class Trie:
    def __init__(self):
        # TODO: implement
        raise NotImplementedError

    def insert(self, word: str) -> None:
        # TODO: implement
        raise NotImplementedError

    def search(self, word: str) -> bool:
        # TODO: implement
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        # TODO: implement
        raise NotImplementedError


if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.starts_with("app") is True
    print("ok")
