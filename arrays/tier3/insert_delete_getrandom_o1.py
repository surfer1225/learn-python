"""Insert Delete GetRandom O(1)
https://leetcode.com/problems/insert-delete-getrandom-o1/

Tier 3 — prepare if you have time · Arrays & Hashing

Design a set supporting `insert`, `remove`, and `get_random` in average O(1).
`get_random` must return each contained element with equal probability.

Hint: a dict gives O(1) lookup but no random indexing; a list gives random
indexing but O(n) removal. Combine them.

Example:
    Input:  insert(1), remove(2), insert(2), get_random()
    Output: True, False, True, 1 or 2

Run: python arrays/tier3/insert_delete_getrandom_o1.py
"""


class RandomizedSet:
    def __init__(self) -> None:
        # TODO: implement
        raise NotImplementedError

    def insert(self, val: int) -> bool:
        """Return True if `val` was not already present."""
        raise NotImplementedError

    def remove(self, val: int) -> bool:
        """Return True if `val` was present."""
        raise NotImplementedError

    def get_random(self) -> int:
        """Return a uniformly random element."""
        raise NotImplementedError


if __name__ == "__main__":
    rs = RandomizedSet()
    assert rs.insert(1) is True
    assert rs.remove(2) is False
    assert rs.insert(2) is True
    assert rs.get_random() in (1, 2)
    assert rs.remove(1) is True
    assert rs.insert(2) is False
    assert rs.get_random() == 2
    print("ok")
