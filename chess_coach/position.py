"""What the tutor is allowed to know about a position.

A language model cannot see a board. It sees whatever this module writes down,
so the ceiling on how well the AI coach can teach is set here — and, more
usefully, so is the ceiling on how badly it can mislead. The important field is
`legal`: the complete list of moves the engine says are available. Handing that
over turns "what should I play?" from a memory question into a selection
question, and it gives `tutor.py` something to check the answer against.

Nothing here talks to the network, and nothing here is presentation. It is the
translation layer between the engine's data structures and the notation every
chess text in the world already uses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from chess.board import Board
from chess.constants import BOARD_SIZE, Color
from chess.game import Game, GameStatus
from chess.pieces import King, Piece, Rook

from .render import movelist
from .san import square_name, to_san

# Standard piece values. Used only to say a material count out loud — no move
# is ever chosen with them.
VALUES = {"Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, "K": 0}

# Where the pieces that matter for castling rights start.
_HOME = {
    Color.WHITE: {"king": (7, 4), "K": (7, 7), "Q": (7, 0)},
    Color.BLACK: {"king": (0, 4), "k": (0, 7), "q": (0, 0)},
}


# --- material --------------------------------------------------------------
def material_count(board: Board) -> int:
    """White's material minus Black's, in pawns."""
    score = 0
    for row in board.squares:
        for piece in row:
            if piece is not None:
                value = VALUES[piece.letter]
                score += value if piece.color is Color.WHITE else -value
    return score


def material_phrase(board: Board) -> str:
    """The material count as a coach would say it."""
    score = material_count(board)
    if score == 0:
        return "level"
    leader = "White" if score > 0 else "Black"
    return f"{leader} +{abs(score)} ({'pawn' if abs(score) == 1 else 'pawns'})"


# --- FEN -------------------------------------------------------------------
def fen(game: Game, history: Sequence[str] = ()) -> str:
    """The position in Forsyth-Edwards Notation.

    FEN is the lingua franca: it is what an engine, a database, and a model
    trained on chess text all expect. The engine stores nothing that FEN's last
    two fields need, so the move counters are derived from `history` — the SAN
    the session has already played. Without a history they come out as 0 and 1,
    which is honest rather than wrong: those fields only govern the fifty-move
    and threefold rules, which this engine does not adjudicate.
    """
    return " ".join(
        (
            _placement(game.board),
            "w" if game.turn is Color.WHITE else "b",
            _castling(game.board),
            square_name(game.board.en_passant_target)
            if game.board.en_passant_target
            else "-",
            str(halfmove_clock(history)),
            str(len(history) // 2 + 1),
        )
    )


def _placement(board: Board) -> str:
    """Ranks 8 down to 1, runs of empty squares collapsed to a digit."""
    ranks = []
    for row in range(BOARD_SIZE):
        text, empty = "", 0
        for col in range(BOARD_SIZE):
            piece = board.squares[row][col]
            if piece is None:
                empty += 1
                continue
            if empty:
                text += str(empty)
                empty = 0
            text += piece.letter if piece.color is Color.WHITE else piece.letter.lower()
        ranks.append(text + (str(empty) if empty else ""))
    return "/".join(ranks)


def _castling(board: Board) -> str:
    """KQkq, from the pieces themselves.

    The engine records castling rights as `has_moved` on the king and the rook
    rather than as four flags, which is the same information stored where it
    cannot drift out of sync with the board. Reading it back is just asking
    whether the right piece is still standing on its home square untouched.
    """
    rights = ""
    for color in (Color.WHITE, Color.BLACK):
        home = _HOME[color]
        king = board.piece_at(home["king"])
        if not (isinstance(king, King) and king.color is color and not king.has_moved):
            continue
        for flag in [f for f in home if f != "king"]:
            rook = board.piece_at(home[flag])
            if isinstance(rook, Rook) and rook.color is color and not rook.has_moved:
                rights += flag
    return rights or "-"


def halfmove_clock(history: Sequence[str]) -> int:
    """Plies since the last capture or pawn move, read off the SAN.

    A pawn move is the only SAN that starts with a lower-case file letter, and
    a capture is the only one containing 'x'. That is enough to count back
    without replaying anything.
    """
    count = 0
    for san in reversed(list(history)):
        if "x" in san or (san[:1].islower() and not san.startswith("O")):
            break
        count += 1
    return count


# --- legal moves -----------------------------------------------------------
def legal_sans(game: Game) -> List[str]:
    """Every legal move for the side to play, in SAN, sorted for stability.

    Sorted because this string lands in a cached prompt prefix: the engine's
    generation order is deterministic today, but sorting means a refactor of
    move generation cannot silently cost every cache hit.
    """
    return sorted(to_san(game, move) for move in game.board.all_legal_moves(game.turn))


# --- the snapshot the tutor is handed --------------------------------------
@dataclass(frozen=True)
class Snapshot:
    """One position, described completely enough to be coached about."""

    fen: str
    history: Tuple[str, ...]
    to_move: str
    legal: Tuple[str, ...]
    material: str
    status: str
    in_check: bool
    studying: Optional[str] = None  # the line being drilled, when there is one
    matches: Tuple[str, ...] = ()  # repertoire lines this position is still in

    @classmethod
    def of(
        cls,
        game: Game,
        history: Sequence[str] = (),
        *,
        studying: Optional[str] = None,
        matches: Sequence[str] = (),
    ) -> "Snapshot":
        return cls(
            fen=fen(game, history),
            history=tuple(history),
            to_move=game.turn.value,
            legal=tuple(legal_sans(game)),
            material=material_phrase(game.board),
            status=_status(game),
            in_check=game.board.is_in_check(game.turn),
            studying=studying,
            matches=tuple(matches),
        )

    @property
    def move_number(self) -> int:
        return len(self.history) // 2 + 1

    def brief(self) -> str:
        """The position as the model receives it.

        Deliberately terse and in a fixed field order. This block is rebuilt
        every ply and sits at the end of the prompt, after the cached system
        text, so its size is paid for on every call.
        """
        lines = [
            f"FEN: {self.fen}",
            f"To move: {self.to_move} (move {self.move_number})",
            f"Material: {self.material}",
            f"Status: {self.status}",
        ]
        if self.history:
            lines.append(f"Moves so far: {movelist(list(self.history))}")
        else:
            lines.append("Moves so far: none, this is the starting position")
        if self.studying:
            lines.append(f"The learner is working on: {self.studying}")
        if self.matches:
            lines.append(f"Still in book for: {', '.join(self.matches)}")
        lines.append(
            f"Legal moves ({len(self.legal)}): {', '.join(self.legal) or 'none'}"
        )
        return "\n".join(lines)


def _status(game: Game) -> str:
    return {
        GameStatus.ONGOING: "ongoing",
        GameStatus.CHECK: f"{game.turn.value} is in check",
        GameStatus.CHECKMATE: f"checkmate, {game.turn.opponent.value} wins",
        GameStatus.STALEMATE: "stalemate, drawn",
    }[game.status]
