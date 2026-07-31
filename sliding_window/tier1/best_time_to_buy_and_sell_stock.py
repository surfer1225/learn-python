"""Best Time to Buy and Sell Stock
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

Tier 1 — must prepare · Sliding Window

You may choose one day to buy and a later day to sell. Return the maximum
profit, or 0 if no profit is possible.

Example:
    Input:  prices = [7, 1, 5, 3, 6, 4]
    Output: 5        # buy at 1, sell at 6

Run: python sliding_window/tier1/best_time_to_buy_and_sell_stock.py
"""


def max_profit(prices: list[int]) -> int:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    assert max_profit([7, 1, 5, 3, 6, 4]) == 5
    assert max_profit([7, 6, 4, 3, 1]) == 0
    assert max_profit([]) == 0
    print("ok")
