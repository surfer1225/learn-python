"""Partition Labels
https://leetcode.com/problems/partition-labels/

Tier 3 — prepare if you have time · Greedy

Partition the string into as many parts as possible so that each letter appears
in at most one part. Return the part sizes.

Example:
    Input:  s = "ababcbacadefegdehijhklij"
    Output: [9, 7, 8]

Run: python greedy/tier3/partition_labels.py
"""


def partition_labels(s: str) -> list[int]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
    assert partition_labels("eccbbbbdec") == [10]
    assert partition_labels("a") == [1]
    print("ok")
