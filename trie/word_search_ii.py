"""Word Search II
https://leetcode.com/problems/word-search-ii/

Given an m x n board of characters and a list of `words`, return all words on
the board (formed from sequentially adjacent cells, no cell reused per word).
"""

from typing import List


def find_words(board: List[List[str]], words: List[str]) -> List[str]:
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
    print("ok")
