"""Shared constants: colors, board geometry, movement directions, and glyphs."""

from __future__ import annotations

from enum import Enum


class Color(Enum):
    """The two sides. `opponent` makes turn-flipping read naturally."""

    WHITE = "white"
    BLACK = "black"

    @property
    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.WHITE else Color.WHITE


BOARD_SIZE = 8

# --- Movement directions, shared by several pieces -------------------------
ORTHOGONAL = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
KING_OFFSETS = ORTHOGONAL + DIAGONAL
KNIGHT_OFFSETS = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]

# --- Unicode glyphs, keyed by (color, piece letter) ------------------------
# White uses the hollow glyphs, black the filled ones; both are drawn in dark
# ink so they read clearly on either square color.
UNICODE_PIECES = {
    (Color.WHITE, "K"): "♔", (Color.WHITE, "Q"): "♕",
    (Color.WHITE, "R"): "♖", (Color.WHITE, "B"): "♗",
    (Color.WHITE, "N"): "♘", (Color.WHITE, "P"): "♙",
    (Color.BLACK, "K"): "♚", (Color.BLACK, "Q"): "♛",
    (Color.BLACK, "R"): "♜", (Color.BLACK, "B"): "♝",
    (Color.BLACK, "N"): "♞", (Color.BLACK, "P"): "♟",
}

# --- GUI appearance --------------------------------------------------------
SQUARE_SIZE = 72
LIGHT_SQUARE = "#f0d9b5"
DARK_SQUARE = "#b58863"
HIGHLIGHT_SELECTED = "#f6eb61"
HIGHLIGHT_MOVE = "#6fa8dc"
PIECE_INK = "#101010"
