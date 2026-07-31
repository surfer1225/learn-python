"""Decode String
https://leetcode.com/problems/decode-string/

Tier 3 — prepare if you have time · Stack

Decode a string encoded as k[encoded_string], where the bracketed section
repeats k times. Encodings nest.

Example:
    Input:  s = "3[a2[c]]"
    Output: "accaccacc"

Run: python stack/tier3/decode_string.py
"""


def decode_string(s: str) -> str:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert decode_string("3[a]2[bc]") == "aaabcbc"
    assert decode_string("3[a2[c]]") == "accaccacc"
    assert decode_string("2[abc]3[cd]ef") == "abcabccdcdcdef"
    print("ok")
