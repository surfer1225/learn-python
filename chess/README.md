# chess

A small desktop chess game built to illustrate **Python packages and modules**,
clean class design, and separation of concerns.

## Run it

From the project root:

```bash
python -m chess
```

A window opens with a full board. Click a piece to select it — its legal moves
appear as blue dots — then click a destination to move. Use **New Game** to reset.

> Needs `tkinter` (bundled with most Python installs). On macOS with Homebrew
> Python: `brew install python-tk`.

## Module layout

The package is deliberately split so that **all rules are pure Python** and the
GUI is a thin layer on top — the logic can be tested with no display.

| Module         | Responsibility                                              |
| -------------- | ----------------------------------------------------------- |
| `constants.py` | Enums (`Color`), board size, movement directions, glyphs    |
| `move.py`      | `Move` — an immutable, comparable value object              |
| `pieces.py`    | `Piece` ABC + `King/Queen/Rook/Bishop/Knight/Pawn`          |
| `board.py`     | Placement, legal-move generation, check/checkmate detection |
| `game.py`      | Turn order and overall `GameStatus`                         |
| `gui.py`       | The tkinter board (presentation only)                       |
| `__main__.py`  | Entry point for `python -m chess`                           |

Dependency direction (arrows point to what a module imports):

```
gui ──▶ game ──▶ board ──▶ pieces ──▶ move, constants
                    └────────────────▶ move, constants
```

## Design notes

- **One question per piece.** Each piece implements `attacked_squares(...)`; the
  base `Piece` turns that into pseudo-legal moves. Only the pawn (whose move and
  attack patterns differ) overrides more.
- **Legality via simulation.** `Board` filters out any move that would leave its
  own king in check by trying it on a deep copy — simple and obviously correct.
- **Immutable moves.** `Move` is a frozen dataclass, so `move in legal_moves`
  just works and the same object round-trips from the GUI back into the engine.
- **Full rules supported:** captures, castling, en passant, promotion
  (with an underpromotion dialog), check, checkmate, and stalemate.

## Tests

```bash
PYTHONPATH=. python tests/test_chess.py      # or: python -m pytest tests/test_chess.py
```
