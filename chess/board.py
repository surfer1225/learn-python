"""The board: piece placement, move generation, and check detection.

The board holds no notion of "whose turn it is" — that belongs to `Game`. Here
we only answer: what is where, which moves are legal, and is a king in check.
"""

from __future__ import annotations

import copy
from typing import List, Optional

from .constants import BOARD_SIZE, Color
from .move import Move, Position
from .pieces import (
    PROMOTION_CLASSES,
    Bishop,
    King,
    Knight,
    Pawn,
    Piece,
    Queen,
    Rook,
)

# Squares a rook stands on at the start, per side, keyed by castle direction.
_BACK_RANK = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class Board:
    def __init__(self) -> None:
        self.squares: List[List[Optional[Piece]]] = [
            [None] * BOARD_SIZE for _ in range(BOARD_SIZE)
        ]
        self.en_passant_target: Optional[Position] = None
        self._setup_start_position()

    def _setup_start_position(self) -> None:
        for col, piece_cls in enumerate(_BACK_RANK):
            self.squares[0][col] = piece_cls(Color.BLACK)
            self.squares[1][col] = Pawn(Color.BLACK)
            self.squares[6][col] = Pawn(Color.WHITE)
            self.squares[7][col] = piece_cls(Color.WHITE)

    # -- simple queries -----------------------------------------------------
    @staticmethod
    def is_on_board(pos: Position) -> bool:
        row, col = pos
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def piece_at(self, pos: Position) -> Optional[Piece]:
        row, col = pos
        return self.squares[row][col]

    def find_king(self, color: Color) -> Optional[Position]:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.squares[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_attacked(self, pos: Position, by_color: Color) -> bool:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.squares[row][col]
                if piece and piece.color == by_color:
                    if pos in piece.attacked_squares(self, (row, col)):
                        return True
        return False

    def is_in_check(self, color: Color) -> bool:
        king_pos = self.find_king(color)
        return king_pos is not None and self.is_attacked(king_pos, color.opponent)

    # -- legal move generation ---------------------------------------------
    def legal_moves(self, pos: Position) -> List[Move]:
        piece = self.piece_at(pos)
        if piece is None:
            return []
        candidates = piece.pseudo_legal_moves(self, pos)
        if isinstance(piece, King):
            candidates += self._castling_moves(pos)
        return [m for m in candidates if not self._leaves_king_in_check(m, piece.color)]

    def all_legal_moves(self, color: Color) -> List[Move]:
        moves: List[Move] = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.squares[row][col]
                if piece and piece.color == color:
                    moves += self.legal_moves((row, col))
        return moves

    def _leaves_king_in_check(self, move: Move, color: Color) -> bool:
        """Try the move on a throwaway copy and see if our king is attacked."""
        trial = copy.deepcopy(self)
        trial.apply(move)
        return trial.is_in_check(color)

    def _castling_moves(self, king_pos: Position) -> List[Move]:
        king = self.piece_at(king_pos)
        row, _ = king_pos
        if king.has_moved or self.is_attacked(king_pos, king.color.opponent):
            return []

        moves = []
        # (rook column, squares that must be empty, squares the king crosses, king's destination)
        plans = [
            (7, [5, 6], [5, 6], 6),        # king-side
            (0, [1, 2, 3], [2, 3], 2),     # queen-side
        ]
        for rook_col, must_be_empty, king_path, dest_col in plans:
            rook = self.piece_at((row, rook_col))
            if not isinstance(rook, Rook) or rook.has_moved:
                continue
            if any(self.piece_at((row, c)) is not None for c in must_be_empty):
                continue
            if any(self.is_attacked((row, c), king.color.opponent) for c in king_path):
                continue
            moves.append(Move(king_pos, (row, dest_col), is_castle=True))
        return moves

    # -- applying a move ----------------------------------------------------
    def apply(self, move: Move) -> None:
        """Apply a move unconditionally (assumes it is legal)."""
        piece = self.piece_at(move.start)
        start_row, start_col = move.start
        end_row, end_col = move.end

        if move.is_en_passant:
            # The captured pawn sits beside the mover, not on the landing square.
            self.squares[start_row][end_col] = None

        # Move the piece.
        self.squares[end_row][end_col] = piece
        self.squares[start_row][start_col] = None

        if move.promotion:
            promoted = PROMOTION_CLASSES[move.promotion](piece.color)
            promoted.has_moved = True
            self.squares[end_row][end_col] = promoted

        if move.is_castle:
            self._move_castling_rook(end_row, end_col)

        # Remember a square available for en passant next turn.
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(end_row - start_row) == 2:
            self.en_passant_target = ((start_row + end_row) // 2, start_col)

        if piece is not None:
            piece.has_moved = True

    def _move_castling_rook(self, row: int, king_dest_col: int) -> None:
        if king_dest_col == 6:            # king-side: rook h -> f
            rook_from, rook_to = 7, 5
        else:                             # queen-side: rook a -> d
            rook_from, rook_to = 0, 3
        rook = self.squares[row][rook_from]
        self.squares[row][rook_to] = rook
        self.squares[row][rook_from] = None
        if rook is not None:
            rook.has_moved = True
