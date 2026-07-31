"""Group Anagrams
https://leetcode.com/problems/group-anagrams/

Given an array of strings `strs`, group the anagrams together.
"""
from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """Group words sharing the same character multiset.

    The sorted string is a canonical form of that multiset, so two words are
    anagrams iff their sorted forms are equal.

    Time: O(n * k log k) — sorting each of n words of length k.
    Space: O(n * k) — n keys of k characters, plus n references in the values.
    """
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for word in strs:
        groups["".join(sorted(word))].append(word)
    return list(groups.values())


if __name__ == "__main__":
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert sorted(sorted(g) for g in result) == sorted(
        sorted(g) for g in [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    )
    print("ok")
