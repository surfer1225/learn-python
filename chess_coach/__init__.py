"""An opening coach built on top of the `chess` package.

    book.py    the repertoire: lines, the idea behind every move, and the traps
    san.py     Standard Algebraic Notation <-> the engine's Move objects
    render.py  terminal board drawing
    coach.py   the three study modes and the REPL
    __main__.py entry point (`python -m chess_coach`)

The engine itself is reused wholesale from `chess/` — legality, check,
castling, en passant and promotion are already correct there, and a coach that
reimplemented them would only introduce disagreements about what is legal.
"""

from .book import LINES, BookMove, Line
from .coach import drill, explore, learn, repl, selftest
from .san import from_san, play_san, replay, to_san

__all__ = [
    "LINES",
    "BookMove",
    "Line",
    "drill",
    "explore",
    "learn",
    "repl",
    "selftest",
    "from_san",
    "play_san",
    "replay",
    "to_san",
]
