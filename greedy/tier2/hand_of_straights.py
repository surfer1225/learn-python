"""Hand of Straights
https://leetcode.com/problems/hand-of-straights/

Tier 2 — good to prepare · Greedy

Can the hand be rearranged into groups of `group_size` consecutive cards?

Example:
    Input:  hand = [1, 2, 3, 6, 2, 3, 4, 7, 8], group_size = 3
    Output: True     # [1,2,3], [2,3,4], [6,7,8]

Run: python greedy/tier2/hand_of_straights.py
"""


def is_n_straight_hand(hand: list[int], group_size: int) -> bool:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert is_n_straight_hand([1, 2, 3, 6, 2, 3, 4, 7, 8], 3) is True
    assert is_n_straight_hand([1, 2, 3, 4, 5], 4) is False
    assert is_n_straight_hand([1, 2, 3, 4], 2) is True
    print("ok")
