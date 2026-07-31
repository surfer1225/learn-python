"""Word Search
https://leetcode.com/problems/word-search/

Tier 1 — must prepare · Backtracking

Return `True` if `word` can be spelled from sequentially adjacent cells of the
board (horizontal/vertical only), without reusing a cell.

Marking and un-marking visited cells in place avoids an extra set.

Example:
    Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
    Output: True

Run: python backtracking/tier1/word_search.py
"""


def exist(board: list[list[str]], word: str) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    assert exist(board, "ABCCED") is True
    assert exist(board, "SEE") is True
    assert exist(board, "ABCB") is False
    print("ok")
