"""Palindrome Partitioning
https://leetcode.com/problems/palindrome-partitioning/

Tier 2 — good to prepare · Backtracking

Partition `s` so that every substring is a palindrome, and return all such
partitionings.

Example:
    Input:  s = "aab"
    Output: [["a", "a", "b"], ["aa", "b"]]

Run: python backtracking/tier2/palindrome_partitioning.py
"""


def partition(s: str) -> list[list[str]]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(partition("aab")) == [["a", "a", "b"], ["aa", "b"]]
    assert partition("a") == [["a"]]
    print("ok")
