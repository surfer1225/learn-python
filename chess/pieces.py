"""Chess pieces.

`Piece` is an abstract base class. Every concrete piece only has to answer one
question — "which squares do I attack from here?" — and the base class turns
that into legal pseudo-moves. Pawns are the exception (their move and attack
patterns differ), so they override more.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from .constants import (
    DIAGONAL,
    KING_OFFSETS,
    KNIGHT_OFFSETS,
    ORTHOGONAL,
    UNICODE_PIECES,
    Color,
)
from .move import Move, Position

if TYPE_CHECKING:  # imported only for type hints -> avoids a circular import
    from .board import Board


class Piece(ABC):
    """Base class for all pieces."""

    letter: str = "?"

    def __init__(self, color: Color) -> None:
        self.color = color
        self.has_moved = False  # needed for castling and the pawn's double step

    @property
    def symbol(self) -> str:
        return UNICODE_PIECES[(self.color, self.letter)]

    @abstractmethod
    def attacked_squares(self, board: "Board", pos: Position) -> List[Position]:
        """Squares this piece attacks (regardless of what occupies them)."""

    def pseudo_legal_moves(self, board: "Board", pos: Position) -> List[Move]:
        """Attacks minus squares blocked by a friendly piece.

        "Pseudo-legal" because it ignores whether the move leaves the king in
        check — the board applies that final filter.
        """
        moves = []
        for square in self.attacked_squares(board, pos):
            target = board.piece_at(square)
            if target is None or target.color != self.color:
                moves.append(Move(pos, square))
        return moves

    # -- helpers shared by the concrete pieces ------------------------------
    def _sliding_attacks(self, board, pos, directions) -> List[Position]:
        squares = []
        row, col = pos
        for d_row, d_col in directions:
            r, c = row + d_row, col + d_col
            while board.is_on_board((r, c)):
                squares.append((r, c))
                if board.piece_at((r, c)) is not None:
                    break  # ray stops at (and includes) the first blocker
                r, c = r + d_row, c + d_col
        return squares

    def _step_attacks(self, board, pos, offsets) -> List[Position]:
        row, col = pos
        return [
            (row + dr, col + dc)
            for dr, dc in offsets
            if board.is_on_board((row + dr, col + dc))
        ]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.color.name})"


class King(Piece):
    letter = "K"

    def attacked_squares(self, board, pos):
        return self._step_attacks(board, pos, KING_OFFSETS)


class Queen(Piece):
    letter = "Q"

    def attacked_squares(self, board, pos):
        return self._sliding_attacks(board, pos, ORTHOGONAL + DIAGONAL)


class Rook(Piece):
    letter = "R"

    def attacked_squares(self, board, pos):
        return self._sliding_attacks(board, pos, ORTHOGONAL)


class Bishop(Piece):
    letter = "B"

    def attacked_squares(self, board, pos):
        return self._sliding_attacks(board, pos, DIAGONAL)


class Knight(Piece):
    letter = "N"

    def attacked_squares(self, board, pos):
        return self._step_attacks(board, pos, KNIGHT_OFFSETS)


class Pawn(Piece):
    letter = "P"

    def _forward(self) -> int:
        # White sits at the bottom (high row index) and marches up the board.
        return -1 if self.color is Color.WHITE else 1

    def _start_row(self) -> int:
        return 6 if self.color is Color.WHITE else 1

    def _promotion_row(self) -> int:
        return 0 if self.color is Color.WHITE else 7

    def attacked_squares(self, board, pos):
        row, col = pos
        forward = self._forward()
        return [
            (row + forward, col + dc)
            for dc in (-1, 1)
            if board.is_on_board((row + forward, col + dc))
        ]

    def pseudo_legal_moves(self, board, pos):
        moves: List[Move] = []
        row, col = pos
        forward = self._forward()

        # Forward one (and two from the starting row) — only onto empty squares.
        one_ahead = (row + forward, col)
        if board.is_on_board(one_ahead) and board.piece_at(one_ahead) is None:
            self._add_forward_move(moves, pos, one_ahead)
            two_ahead = (row + 2 * forward, col)
            if row == self._start_row() and board.piece_at(two_ahead) is None:
                moves.append(Move(pos, two_ahead))

        # Diagonal captures, including en passant.
        for square in self.attacked_squares(board, pos):
            target = board.piece_at(square)
            if target is not None and target.color != self.color:
                self._add_forward_move(moves, pos, square)
            elif square == board.en_passant_target:
                moves.append(Move(pos, square, is_en_passant=True))

        return moves

    def _add_forward_move(self, moves, start, end) -> None:
        """Emit a move, expanding into the four promotion choices on the last rank."""
        if end[0] == self._promotion_row():
            for promo in ("Q", "R", "B", "N"):
                moves.append(Move(start, end, promotion=promo))
        else:
            moves.append(Move(start, end))


# Maps a promotion letter to its class, used by the board when a pawn promotes.
PROMOTION_CLASSES = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}
