"""An opening coach built on top of the `chess` package.

    book.py     the repertoire: lines, the idea behind every move, and the traps
    gambits.py  the gambits: sacrifice ply, cost, compensation, verdict
    san.py      Standard Algebraic Notation <-> the engine's Move objects
    position.py FEN and the legal move list — the position as the AI coach sees it
    llm.py      the connection to the model, and a fake one for the tests
    tutor.py    the AI coach: prompts in, engine-checked answers out
    render.py   terminal board drawing
    coach.py    the four study modes and the REPL
    __main__.py entry point (`python -m chess_coach`)

The engine itself is reused wholesale from `chess/` — legality, check,
castling, en passant and promotion are already correct there, and a coach that
reimplemented them would only introduce disagreements about what is legal.

The AI coach obeys the same rule from the other direction. A language model
will eventually name a move that is not on the board, so no move it produces
reaches the learner without `chess/` agreeing that it can be played.
"""

from .book import LINES, BookMove, Line
from .coach import drill, explore, learn, repl, selftest, spar
from .llm import Config, LLMUnavailable
from .position import Snapshot, fen, legal_sans
from .san import from_san, play_san, replay, to_san
from .tutor import Answer, Tutor

__all__ = [
    "LINES",
    "Answer",
    "BookMove",
    "Config",
    "LLMUnavailable",
    "Line",
    "Snapshot",
    "Tutor",
    "drill",
    "explore",
    "fen",
    "from_san",
    "learn",
    "legal_sans",
    "play_san",
    "replay",
    "repl",
    "selftest",
    "spar",
    "to_san",
]
