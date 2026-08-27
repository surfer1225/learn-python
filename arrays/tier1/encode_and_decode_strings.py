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
    """Length-prefix each string as `<len>#<payload>`.

    No character needs escaping: the length says exactly how many characters
    the payload occupies, so a '#' or a digit inside a payload can never be
    mistaken for framing. The '#' only terminates the digit run.

    Time O(n) over total characters · Space O(n) for the output.
    """
    return "".join(f"{len(s)}#{s}" for s in strs)


def decode(s: str) -> list[str]:
    """Inverse of `encode`.

    Read digits up to the next '#', then consume exactly that many characters
    verbatim and jump past them — the payload is never scanned.

    Time O(n) over total characters · Space O(n) for the output.
    """
    out: list[str] = []
    i = 0

    while i < len(s):
        j = s.index("#", i)  # end of the digit run
        length = int(s[i:j])
        start = j + 1
        out.append(s[start : start + length])
        i = start + length

    return out


if __name__ == "__main__":
    cases = [
        [],
        [""],
        ["neet", "code", "love", "you"],
        ["we#say", ":", "#3", "yes"],
        ["", ""],  # distinct from [] and from [""]
        ["#", "##", "###"],  # delimiter as payload
        ["12#34"],  # payload that looks like framing
        ["0#"],  # payload that looks like an empty string
        ["a" * 1000, ""],  # multi-digit length
        ["\n", "\t", "\\", ","],  # whitespace and would-be escapes
        ["héllo", "😀", "é"],  # non-ASCII, emoji, combining mark
    ]
    for case in cases:
        assert decode(encode(case)) == case, case

    # Encoding must be injective: distinct inputs -> distinct outputs.
    seen: dict[str, list[str]] = {}
    for case in cases:
        enc = encode(case)
        assert seen.setdefault(enc, case) == case, (seen[enc], case)

    print("ok")
