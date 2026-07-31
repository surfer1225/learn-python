"""Word Search II
https://leetcode.com/problems/word-search-ii/

Tier 3 — prepare if you have time · Tries

Given an m x n board of letters and a list of words, return all words that can
be formed from sequentially adjacent cells (no cell reused within a word).

Running Word Search once per word is too slow. Put the words in a trie and DFS
the board once.

Example:
    Input:  board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
            words = ["oath", "pea", "eat", "rain"]
    Output: ["eat", "oath"]

Run: python trie/tier3/word_search_ii.py
"""


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    board = [
        ["o", "a", "a", "n"],
        ["e", "t", "a", "e"],
        ["i", "h", "k", "r"],
        ["i", "f", "l", "v"],
    ]
    assert sorted(find_words(board, ["oath", "pea", "eat", "rain"])) == ["eat", "oath"]
    assert find_words([["a", "b"], ["c", "d"]], ["abcb"]) == []
    print("ok")
