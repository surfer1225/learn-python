"""The tkinter desktop board — the presentation layer.

Interaction model: click a piece to select it (its legal destinations light up
as dots), then click a destination to move. Click elsewhere to reselect.

This module knows nothing about chess rules; it only draws `Game` state and
forwards clicks. All rule logic lives in the pure-Python modules.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import List, Optional

from .constants import (
    BOARD_SIZE,
    DARK_SQUARE,
    HIGHLIGHT_MOVE,
    HIGHLIGHT_SELECTED,
    LIGHT_SQUARE,
    PIECE_INK,
    SQUARE_SIZE,
)
from .game import Game, GameStatus
from .move import Move, Position


class ChessGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Chess")
        self.root.resizable(False, False)

        self.game = Game()
        self.selected: Optional[Position] = None
        self.legal_for_selected: List[Move] = []

        size = BOARD_SIZE * SQUARE_SIZE
        self.canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        self.status_label = tk.Label(root, font=("Helvetica", 14), pady=6)
        self.status_label.pack(fill="x")

        tk.Button(root, text="New Game", command=self._new_game).pack(pady=(0, 8))

        self._render()

    # -- event handling -----------------------------------------------------
    def _on_click(self, event: tk.Event) -> None:
        if self.game.is_over:
            return
        pos = (event.y // SQUARE_SIZE, event.x // SQUARE_SIZE)
        if not (0 <= pos[0] < BOARD_SIZE and 0 <= pos[1] < BOARD_SIZE):
            return

        if self.selected is not None:
            matches = [m for m in self.legal_for_selected if m.end == pos]
            if matches:
                self._play(matches)
                return
        self._select(pos)

    def _select(self, pos: Position) -> None:
        moves = self.game.legal_moves(pos)
        self.selected = pos if moves else None
        self.legal_for_selected = moves
        self._render()

    def _play(self, matches: List[Move]) -> None:
        move = matches[0] if len(matches) == 1 else self._ask_promotion(matches)
        self.game.move(move)
        self.selected = None
        self.legal_for_selected = []
        self._render()
        if self.game.is_over:
            messagebox.showinfo("Game over", self.status_label.cget("text"))

    def _new_game(self) -> None:
        self.game = Game()
        self.selected = None
        self.legal_for_selected = []
        self._render()

    def _ask_promotion(self, matches: List[Move]) -> Move:
        chosen = {"letter": "Q"}
        dialog = tk.Toplevel(self.root)
        dialog.title("Promote to")
        dialog.transient(self.root)
        dialog.grab_set()

        def pick(letter: str) -> None:
            chosen["letter"] = letter
            dialog.destroy()

        for letter, name in [("Q", "Queen"), ("R", "Rook"), ("B", "Bishop"), ("N", "Knight")]:
            tk.Button(dialog, text=name, width=12, command=lambda l=letter: pick(l)).pack(
                padx=12, pady=4
            )
        self.root.wait_window(dialog)

        return next((m for m in matches if m.promotion == chosen["letter"]), matches[0])

    # -- drawing ------------------------------------------------------------
    def _render(self) -> None:
        self.canvas.delete("all")
        self._draw_squares()
        if self.selected is not None:
            self._shade(self.selected, HIGHLIGHT_SELECTED)
            for move in self.legal_for_selected:
                self._draw_move_hint(move.end)
        self._draw_pieces()
        self._update_status_text()

    def _draw_squares(self) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                self._shade((row, col), color)

    def _draw_pieces(self) -> None:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board.piece_at((row, col))
                if piece is not None:
                    self.canvas.create_text(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                        text=piece.symbol,
                        fill=PIECE_INK,
                        font=("Arial", SQUARE_SIZE // 2),
                    )

    def _shade(self, pos: Position, color: str) -> None:
        row, col = pos
        x1, y1 = col * SQUARE_SIZE, row * SQUARE_SIZE
        self.canvas.create_rectangle(
            x1, y1, x1 + SQUARE_SIZE, y1 + SQUARE_SIZE, fill=color, outline=color
        )

    def _draw_move_hint(self, pos: Position) -> None:
        row, col = pos
        cx = col * SQUARE_SIZE + SQUARE_SIZE // 2
        cy = row * SQUARE_SIZE + SQUARE_SIZE // 2
        r = SQUARE_SIZE // 7
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=HIGHLIGHT_MOVE, outline="")

    def _update_status_text(self) -> None:
        turn = self.game.turn.name.capitalize()
        status = self.game.status
        if status is GameStatus.CHECKMATE:
            text = f"Checkmate — {self.game.winner.name.capitalize()} wins!"
        elif status is GameStatus.STALEMATE:
            text = "Stalemate — it's a draw."
        elif status is GameStatus.CHECK:
            text = f"{turn} to move — check!"
        else:
            text = f"{turn} to move"
        self.status_label.config(text=text)


def run() -> None:
    """Create the window and start the tkinter event loop."""
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()
