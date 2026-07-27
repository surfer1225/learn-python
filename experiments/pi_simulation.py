"""Simulating the computation of pi.

Three different approaches, each showing off a different Python feature:

1. Monte Carlo   -> random sampling (the `random` module)
2. Leibniz       -> an infinite series via a generator
3. math.pi       -> the ground-truth reference

Run it:
    python experiments/pi_simulation.py
"""

import math
import random
from typing import Iterator


def monte_carlo_pi(samples: int = 1_000_000) -> float:
    """Estimate pi by throwing darts at a unit square.

    A quarter circle of radius 1 has area pi/4, and the enclosing unit square
    has area 1. So (points inside circle / total points) -> pi/4.
    """
    inside = 0
    for _ in range(samples):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4 * inside / samples


def leibniz_terms() -> Iterator[float]:
    """Yield the terms of the Leibniz series: 1 - 1/3 + 1/5 - 1/7 + ...

    A generator: it produces terms lazily, one at a time, forever.
    """
    denominator = 1
    sign = 1
    while True:
        yield sign / denominator
        denominator += 2
        sign *= -1


def leibniz_pi(terms: int = 1_000_000) -> float:
    """Estimate pi by summing the first `terms` Leibniz terms (series -> pi/4)."""
    gen = leibniz_terms()
    total = sum(next(gen) for _ in range(terms))
    return 4 * total


def main() -> None:
    reference = math.pi
    print(f"{'method':<14}{'estimate':<20}{'abs error':<12}")
    print("-" * 46)

    estimates = {
        "monte carlo": monte_carlo_pi(),
        "leibniz": leibniz_pi(),
        "math.pi": reference,
    }
    for name, value in estimates.items():
        error = abs(value - reference)
        print(f"{name:<14}{value:<20.10f}{error:<12.2e}")


if __name__ == "__main__":
    main()
