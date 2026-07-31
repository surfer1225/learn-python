"""Design Add and Search Words Data Structure
https://leetcode.com/problems/design-add-and-search-words-data-structure/

Tier 2 — good to prepare · Tries

Support `add_word` and `search`, where a '.' in the search string matches any
single letter.

The wildcard turns the lookup into a DFS over the trie.

Example:
    Input:  add("bad"), add("dad"), search("pad"), search(".ad"), search("b..")
    Output: False, True, True

Run: python trie/tier2/design_add_and_search_words.py
"""


class WordDictionary:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def add_word(self, word: str) -> None:
        raise NotImplementedError

    def search(self, word: str) -> bool:
        """'.' matches any single character."""
        raise NotImplementedError


if __name__ == "__main__":
    words = WordDictionary()
    for word in ("bad", "dad", "mad"):
        words.add_word(word)
    assert words.search("pad") is False
    assert words.search("bad") is True
    assert words.search(".ad") is True
    assert words.search("b..") is True
    assert words.search("b...") is False
    print("ok")
