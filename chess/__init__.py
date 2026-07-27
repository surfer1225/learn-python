"""A small, well-structured chess game.

The package is split into focused modules to illustrate how Python code is
organized into modules and packages:

    constants.py  -> shared enums, sizes, colors, movement directions
    move.py       -> the immutable Move value object
    pieces.py     -> Piece base class and the six concrete piece types
    board.py      -> board state, move generation, check/checkmate logic
    game.py       -> turn management and high-level game status
    gui.py        -> the tkinter desktop board (presentation layer)
    __main__.py   -> entry point (`python -m chess`)

Only the game logic (everything except gui.py) is pure Python with no external
dependencies, which keeps it easy to test in isolation from the UI.
"""

from .constants import Color
from .game import Game, GameStatus
from .move import Move

__all__ = ["Color", "Game", "GameStatus", "Move"]
