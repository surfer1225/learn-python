"""The Move value object.

A frozen dataclass is a good fit: a move is immutable data, is comparable by
value (so `move in legal_moves` works), and is hashable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

# A board position is a (row, col) pair. Row 0 is the top (black's back rank).
Position = Tuple[int, int]


@dataclass(frozen=True)
class Move:
    start: Position
    end: Position
    is_castle: bool = False
    is_en_passant: bool = False
    promotion: Optional[str] = None  # piece letter to promote a pawn into

    def __str__(self) -> str:
        return f"{_algebraic(self.start)}{_algebraic(self.end)}"


def _algebraic(pos: Position) -> str:
    """Convert (row, col) to algebraic notation like 'e4' for readable output."""
    row, col = pos
    file = chr(ord("a") + col)
    rank = 8 - row
    return f"{file}{rank}"
