"""Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings `strs`, group the anagrams together.
"""

from typing import List


def group_anagrams(strs: List[str]) -> List[List[str]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(sorted(g) for g in result) == sorted(
        sorted(g) for g in [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    )
    print("ok")
