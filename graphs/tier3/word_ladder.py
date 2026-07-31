"""Word Ladder
https://leetcode.com/problems/word-ladder/

Tier 3 — prepare if you have time · Graphs

Transform `begin_word` into `end_word` one letter at a time, where every
intermediate word must be in `word_list`. Return the number of words in the
shortest sequence, or 0.

BFS on an implicit graph. The follow-up is bidirectional BFS.

Example:
    Input:  begin = "hit", end = "cog", words = ["hot","dot","dog","lot","log","cog"]
    Output: 5

Run: python graphs/tier3/word_ladder.py
"""


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2
    print("ok")
