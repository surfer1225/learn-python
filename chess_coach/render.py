"""Terminal board rendering.

Kept deliberately separate from the coaching logic so the session can be driven
headlessly in tests: nothing here is imported for correctness, only for looks.
"""

from __future__ import annotations

import os
import re
import sys
from typing import Iterable, Optional, Set

from chess.board import Board
from chess.constants import BOARD_SIZE, Color
from chess.move import Position

from .san import square_name

# 256-colour ANSI. Chosen to echo the tkinter GUI's palette in constants.py.
_LIGHT = "\x1b[48;5;180m"
_DARK = "\x1b[48;5;95m"
_LAST = "\x1b[48;5;107m"  # square touched by the most recent move
_HINT = "\x1b[48;5;110m"  # square the coach is pointing at
_WHITE_INK = "\x1b[38;5;231m"
_BLACK_INK = "\x1b[38;5;232m"
_RESET = "\x1b[0m"

BOLD = "\x1b[1m"
DIM = "\x1b[2m"
GREEN = "\x1b[38;5;71m"
RED = "\x1b[38;5;167m"
YELLOW = "\x1b[38;5;179m"
CYAN = "\x1b[38;5;73m"


def color_enabled() -> bool:
    """Respect NO_COLOR and non-tty output, the way well-behaved CLIs do."""
    if os.environ.get("NO_COLOR"):
        return False
    return sys.stdout.isatty()


def paint(text: str, *codes: str) -> str:
    if not color_enabled():
        return text
    return "".join(codes) + text + _RESET


def board_lines(
    board: Board,
    *,
    flipped: bool = False,
    highlight: Optional[Iterable[Position]] = None,
    hint: Optional[Iterable[Position]] = None,
) -> list[str]:
    """Render the board as a list of printable lines.

    `flipped` shows it from Black's side — worth doing when drilling a Black
    repertoire, since a defence looks different from the wrong side of the
    board and you want the pattern stored the way you will meet it.
    """
    lit: Set[Position] = set(highlight or ())
    pointed: Set[Position] = set(hint or ())
    use_color = color_enabled()

    rows = range(BOARD_SIZE - 1, -1, -1) if flipped else range(BOARD_SIZE)
    cols = range(BOARD_SIZE - 1, -1, -1) if flipped else range(BOARD_SIZE)

    lines = []
    for row in rows:
        cells = []
        for col in cols:
            piece = board.squares[row][col]
            glyph = piece.symbol if piece else " "
            if not use_color:
                cells.append(f" {glyph if piece else '.'} ")
                continue

            if (row, col) in pointed:
                bg = _HINT
            elif (row, col) in lit:
                bg = _LAST
            else:
                bg = _LIGHT if (row + col) % 2 == 0 else _DARK
            ink = _WHITE_INK if piece and piece.color is Color.WHITE else _BLACK_INK
            cells.append(f"{bg}{ink} {glyph} {_RESET}")

        lines.append(f" {8 - row} " + "".join(cells))

    files = "abcdefgh" if not flipped else "hgfedcba"
    lines.append("   " + "".join(f" {f} " for f in files))
    return lines


def board_text(board: Board, **kwargs) -> str:
    return "\n".join(board_lines(board, **kwargs))


def move_squares(move) -> list[Position]:
    return [move.start, move.end]


def format_move_pair(number: int, white: str, black: Optional[str]) -> str:
    """'1. e4 e5' — the way a book prints a full move."""
    return f"{number}. {white}" + (f" {black}" if black else "")


def movelist(sans: list[str], *, start: int = 1, black_first: bool = False) -> str:
    """Render a flat list of SAN plies as numbered move pairs.

    `start` and `black_first` are for variations, which do not begin at move
    one and need not begin with White. A line the coach offers from move 12 as
    Black prints as '12... Nxe4  13. Bd3'; numbering it from one would point
    the learner at the wrong part of their own game.
    """
    out = []
    index, number = 0, start
    if black_first and sans:
        out.append(f"{number}... {sans[0]}")
        index, number = 1, number + 1
    while index < len(sans):
        white = sans[index]
        black = sans[index + 1] if index + 1 < len(sans) else None
        out.append(format_move_pair(number, white, black))
        index, number = index + 2, number + 1
    return "  ".join(out)


_EMPHASIS = re.compile(r"\*([^*]+)\*")


def emphasize(text: str) -> str:
    """Render *emphasis* as terminal bold, or strip the markers when piping.

    The book uses asterisks because the commentary is written to be read as
    prose; without this the learner would see literal asterisks on screen.
    """
    if not color_enabled():
        return _EMPHASIS.sub(r"\1", text)
    return _EMPHASIS.sub(lambda m: BOLD + m.group(1) + _RESET, text)


def wrap(
    text: str,
    width: int = 76,
    indent: str = "",
    first_indent: Optional[str] = None,
) -> str:
    """Word wrap preserving `indent` on every line.

    `first_indent` overrides the prefix of the first line only, which gives
    hanging indents for bullets: pass "  - " and "    " so wrapped text lines
    up under the text rather than under the marker.
    """
    words = text.split()
    if not words:
        return ""
    head = indent if first_indent is None else first_indent
    lines, current = [], head + words[0]
    for word in words[1:]:
        if len(current) + 1 + len(word) > width:
            lines.append(current)
            current = indent + word
        else:
            current += " " + word
    lines.append(current)
    return "\n".join(lines)


def bullet(text: str, indent: str = "     ", marker: str = "- ") -> str:
    """A wrapped bullet whose continuation lines hang under the text."""
    return wrap(text, indent=indent + " " * len(marker), first_indent=indent + marker)


def square_list(positions: Iterable[Position]) -> str:
    return ", ".join(square_name(p) for p in positions)
