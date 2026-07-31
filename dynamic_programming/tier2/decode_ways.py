"""Decode Ways
https://leetcode.com/problems/decode-ways/

Tier 2 — good to prepare · Dynamic Programming

'A' maps to "1" ... 'Z' to "26". Return the number of ways to decode a digit
string.

Leading zeros are the trap: "06" is not a valid encoding of 'F'.

Example:
    Input:  s = "226"
    Output: 3        # "BZ", "VF", "BBF"

Run: python dynamic_programming/tier2/decode_ways.py
"""


def num_decodings(s: str) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert num_decodings("12") == 2
    assert num_decodings("226") == 3
    assert num_decodings("06") == 0
    assert num_decodings("10") == 1
    print("ok")
