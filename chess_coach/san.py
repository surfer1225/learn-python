"""Standard Algebraic Notation (SAN) <-> the engine's `Move` objects.

Every chess book writes moves as `Nf3`, `exd5`, `O-O`, `Bb4+`. The engine in
`chess/` speaks `Move` objects over (row, col) pairs. This module translates.

Only one direction is really implemented. `to_san` renders a Move; `from_san`
parses by generating every legal move, rendering each to SAN, and matching the
string. That is O(legal moves) per parse — irrelevant at ~30 moves a position —
and it buys something valuable: the two directions can never disagree. There is
no separate grammar to keep in sync, so disambiguation, capture marks, check
suffixes, and castling are automatically consistent both ways.
"""

from __future__ import annotations

from typing import List, Optional

from chess.board import Board
from chess.constants import BOARD_SIZE, Color
from chess.game import Game
from chess.move import Move, Position
from chess.pieces import PROMOTION_CLASSES, Pawn

# Characters that carry no information for matching: check/mate marks, the
# annotator's punctuation, and the capture 'x'. Dropping 'x' from both sides of
# the comparison also lets a learner type "ed5" for "exd5" without being
# scolded. It is safe: a destination square is either occupied or not, so two
# legal moves to the same square can never differ in capture status.
_NOISE = "+#!?x "


def square_name(pos: Position) -> str:
    """(row, col) -> 'e4'. Row 0 is the top of the board (rank 8)."""
    row, col = pos
    return f"{chr(ord('a') + col)}{8 - row}"


def square_index(name: str) -> Position:
    """'e4' -> (row, col). Inverse of `square_name`."""
    file_ch, rank_ch = name[0], name[1]
    return (8 - int(rank_ch), ord(file_ch) - ord("a"))


def normalize(text: str) -> str:
    """Strip everything that does not distinguish one legal move from another."""
    cleaned = text.strip().replace("0", "O").replace("e.p.", "")
    for ch in _NOISE:
        cleaned = cleaned.replace(ch, "")
    return cleaned


def to_san(game: Game, move: Move) -> str:
    """Render `move` in the position `game` as SAN.

    The move must be legal in this position; disambiguation is computed against
    the other legal moves, so an illegal move would produce nonsense.
    """
    piece = game.board.piece_at(move.start)
    if piece is None:
        raise ValueError(f"no piece on {square_name(move.start)}")

    if move.is_castle:
        body = "O-O" if move.end[1] == 6 else "O-O-O"
    elif isinstance(piece, Pawn):
        body = _pawn_san(game, move)
    else:
        body = _piece_san(game, move, piece)

    return body + _check_suffix(game, move, piece.color)


def from_san(game: Game, text: str) -> Optional[Move]:
    """Find the legal move for the side to play whose SAN matches `text`.

    Returns None if nothing matches (illegal move, or a typo).
    """
    wanted = normalize(text)
    if not wanted:
        return None
    for move in game.board.all_legal_moves(game.turn):
        if normalize(to_san(game, move)) == wanted:
            return move
    return None


def play_san(game: Game, text: str) -> Optional[Move]:
    """Parse `text` and play it. Returns the move played, or None if invalid."""
    move = from_san(game, text)
    if move is not None and game.move(move):
        return move
    return None


def replay(moves: List[str]) -> Game:
    """Play a list of SAN moves from the start position.

    Raises ValueError on the first move that does not parse — which is exactly
    what we want the book's self-check to do.
    """
    game = Game()
    for ply, san in enumerate(moves, start=1):
        if play_san(game, san) is None:
            raise ValueError(f"illegal move at ply {ply}: {san!r}")
    return game


# -- rendering helpers ------------------------------------------------------
def _pawn_san(game: Game, move: Move) -> str:
    captures = move.is_en_passant or game.board.piece_at(move.end) is not None
    dest = square_name(move.end)
    body = f"{chr(ord('a') + move.start[1])}x{dest}" if captures else dest
    if move.promotion:
        body += f"={move.promotion}"
    return body


def _piece_san(game: Game, move: Move, piece) -> str:
    body = piece.letter + _disambiguator(game, move, piece)
    if game.board.piece_at(move.end) is not None:
        body += "x"
    return body + square_name(move.end)


def _disambiguator(game: Game, move: Move, piece) -> str:
    """The shortest prefix that identifies which piece is moving.

    Standard rule: prefer the file, fall back to the rank, and only give the
    whole square when two rivals share both a file and a rank with us (three
    queens, say). Needed for positions like Nbxd2 where either knight can land.

    Only same-type pieces are asked for their legal moves. Generating *all*
    legal moves here would be correct but quadratic, and `to_san` sits in the
    inner loop of `from_san`.
    """
    board = game.board
    rivals: List[Position] = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            other = board.squares[row][col]
            if (
                other is not None
                and (row, col) != move.start
                and other.color is piece.color
                and type(other) is type(piece)
                and any(m.end == move.end for m in board.legal_moves((row, col)))
            ):
                rivals.append((row, col))

    if not rivals:
        return ""

    file_is_unique = not any(r[1] == move.start[1] for r in rivals)
    rank_is_unique = not any(r[0] == move.start[0] for r in rivals)

    if file_is_unique:
        return chr(ord("a") + move.start[1])
    if rank_is_unique:
        return str(8 - move.start[0])
    return square_name(move.start)


def _board_after(board: Board, move: Move) -> Board:
    """The position after `move`, without deep-copying every piece.

    `Board.apply` sets `piece.has_moved`, so it cannot be run against a shallow
    copy — it would corrupt the real position's castling rights. Here the grid
    is copied and the pieces are only *re-placed*, never mutated. That is
    enough to answer "is the enemy king attacked?", which is all we need.
    """
    clone = Board.__new__(Board)
    clone.squares = [row[:] for row in board.squares]
    clone.en_passant_target = None

    start_row, start_col = move.start
    end_row, end_col = move.end
    piece = clone.squares[start_row][start_col]

    if move.is_en_passant:
        clone.squares[start_row][end_col] = None

    clone.squares[end_row][end_col] = piece
    clone.squares[start_row][start_col] = None

    if move.promotion:
        clone.squares[end_row][end_col] = PROMOTION_CLASSES[move.promotion](piece.color)

    if move.is_castle:
        rook_from, rook_to = (7, 5) if end_col == 6 else (0, 3)
        clone.squares[end_row][rook_to] = clone.squares[end_row][rook_from]
        clone.squares[end_row][rook_from] = None

    return clone


def _check_suffix(game: Game, move: Move, mover: Color) -> str:
    """'+' for check, '#' for mate, '' otherwise.

    The mate test is the expensive one (it generates every enemy reply), so it
    only runs once we already know the move gives check — a rare case.
    """
    after = _board_after(game.board, move)
    if not after.is_in_check(mover.opponent):
        return ""
    return "+" if after.all_legal_moves(mover.opponent) else "#"
