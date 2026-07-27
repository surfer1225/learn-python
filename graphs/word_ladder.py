"""Word Ladder
https://leetcode.com/problems/word-ladder/

Return the number of words in the shortest transformation sequence from
`beginWord` to `endWord`, changing one letter at a time, where each intermediate
word must be in `wordList`. Return 0 if no such sequence exists.
"""

from typing import List


def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    print("ok")
