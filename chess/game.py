"""Game controller: whose turn it is and what the overall status is.

This is the thin layer the GUI talks to. It never reaches into board internals
beyond the small, intentional public surface of `Board`.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import List, Optional

from .board import Board
from .constants import Color
from .move import Move, Position


class GameStatus(Enum):
    ONGOING = auto()
    CHECK = auto()
    CHECKMATE = auto()
    STALEMATE = auto()


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.turn = Color.WHITE
        self.status = GameStatus.ONGOING
        self.winner: Optional[Color] = None

    def legal_moves(self, pos: Position) -> List[Move]:
        """Legal moves for the piece at `pos`, but only if it's that side's turn."""
        piece = self.board.piece_at(pos)
        if piece is None or piece.color != self.turn:
            return []
        return self.board.legal_moves(pos)

    def move(self, move: Move) -> bool:
        """Play `move` if legal. Returns True on success, False otherwise."""
        if self.is_over or move not in self.legal_moves(move.start):
            return False
        self.board.apply(move)
        self.turn = self.turn.opponent
        self._update_status()
        return True

    @property
    def is_over(self) -> bool:
        return self.status in (GameStatus.CHECKMATE, GameStatus.STALEMATE)

    def _update_status(self) -> None:
        has_moves = bool(self.board.all_legal_moves(self.turn))
        in_check = self.board.is_in_check(self.turn)
        if not has_moves:
            self.status = GameStatus.CHECKMATE if in_check else GameStatus.STALEMATE
            self.winner = self.turn.opponent if in_check else None
        else:
            self.status = GameStatus.CHECK if in_check else GameStatus.ONGOING
