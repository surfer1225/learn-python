"""Encode and Decode Strings
https://leetcode.com/problems/encode-and-decode-strings/

Tier 1 — must prepare · Arrays & Hashing

Design an algorithm to encode a list of strings into a single string, and decode
that string back into the original list. Strings may contain any characters —
including whatever delimiter you are tempted to use.

Example:
    Input:  ["neet", "code", "love", "you"]
    Output: ["neet", "code", "love", "you"]   # after encode then decode

Run: python arrays/tier1/encode_and_decode_strings.py
"""


def encode(strs: list[str]) -> str:
    # TODO: implement
    raise NotImplementedError


def decode(s: str) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    for case in ([], [""], ["neet", "code", "love", "you"], ["we#say", ":", "#3", "yes"]):
        assert decode(encode(case)) == case
    print("ok")
