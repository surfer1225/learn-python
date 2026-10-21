"""GPU Credits

OpenAI-style multi-part coding question. Reported in OpenAI phone screens as
"implement a GPU credit management system" (Aced, 2026) and "design a credit
tracking service for user token balances" (Hello Interview L5 list).

Format: 60 minutes, CoderPad, parts revealed one at a time. Graded on working
code, code quality, edge cases and tests. Finish each part cleanly before the
next.

Part 1 — credits, expiry, spending
    add_credit(credit_id, amount, timestamp, expiration)
        Grants `amount` credits usable at any time t with
        timestamp <= t < timestamp + expiration.
    use_credit(timestamp, amount) -> bool
        Spends `amount` from credits active at `timestamp`, all or nothing.
        Draw from the credit that expires soonest first. Returns False and
        spends nothing if the active balance is too small.
    get_balance(timestamp) -> int
        Total unspent credit active at `timestamp`.
    In Part 1, calls arrive in non-decreasing timestamp order.

Part 2 — out-of-order calls
    Calls may now arrive in any timestamp order. Every result must be as if
    all recorded events were replayed in timestamp order (adds before uses at
    the same timestamp, otherwise arrival order). A use that can't be fully
    covered at its point in the replay is skipped. use_credit returns its
    outcome given the events known when it is called — a late-arriving add
    can later make an earlier failed use succeed in the replay.

Part 3 — scale (discussed live, no self-check)
    10^5 interleaved calls. What is your complexity per call? Make
    get_balance and use_credit faster than replaying everything each time.

Example (Part 1):
    add_credit("a", 10, 0, 10)    active [0, 10)
    add_credit("b", 5, 2, 3)      active [2, 5)
    get_balance(2)    -> 15
    use_credit(3, 4)  -> True     takes 4 from "b" (expires first)
    get_balance(5)    -> 10       "b" has expired

Run: python openai_coding/gpu_credits.py
"""


class GPUCredits:
    def add_credit(self, credit_id: str, amount: int, timestamp: int, expiration: int) -> None:
        # TODO: implement
        raise NotImplementedError

    def use_credit(self, timestamp: int, amount: int) -> bool:
        # TODO: implement
        raise NotImplementedError

    def get_balance(self, timestamp: int) -> int:
        # TODO: implement
        raise NotImplementedError


def check_part1() -> None:
    c = GPUCredits()
    c.add_credit("a", 10, 0, 10)
    c.add_credit("b", 5, 2, 3)
    assert c.get_balance(1) == 10
    assert c.get_balance(2) == 15
    assert c.use_credit(3, 4) is True
    assert c.get_balance(3) == 11
    assert c.get_balance(5) == 10
    assert c.use_credit(6, 11) is False
    assert c.get_balance(6) == 10
    assert c.use_credit(9, 10) is True
    assert c.get_balance(9) == 0
    assert c.get_balance(10) == 0


def check_part2() -> None:
    c = GPUCredits()
    c.add_credit("a", 3, 10, 10)
    assert c.use_credit(12, 5) is False
    c.add_credit("b", 4, 5, 10)
    assert c.get_balance(7) == 4
    assert c.get_balance(12) == 2
    assert c.get_balance(16) == 2
    assert c.get_balance(20) == 0
    c.add_credit("c", 1, 11, 100)
    assert c.get_balance(11) == 8
    assert c.get_balance(12) == 3


if __name__ == "__main__":
    check_part1()
    print("part 1 ok")
    check_part2()
    print("part 2 ok")
