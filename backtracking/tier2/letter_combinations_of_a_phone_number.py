"""Letter Combinations of a Phone Number
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Tier 2 — good to prepare · Backtracking

Given digits 2-9, return all letter combinations the number could spell, using
the standard telephone keypad mapping.

Example:
    Input:  digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Run: python backtracking/tier2/letter_combinations_of_a_phone_number.py
"""


def letter_combinations(digits: str) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert sorted(letter_combinations("23")) == [
        "ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf",
    ]
    assert letter_combinations("") == []
    assert sorted(letter_combinations("2")) == ["a", "b", "c"]
    print("ok")
