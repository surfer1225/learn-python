"""Engine tests for the chess package (no GUI / display needed).

Run from the project root:
    PYTHONPATH=. python tests/test_chess.py
    # or
    python -m pytest tests/test_chess.py
"""

from chess import Color, Game, GameStatus
from chess.move import Move


def _find(game: Game, start, end) -> Move:
    """Pick the legal move from `start` to `end` (auto-queen on promotion)."""
    options = [m for m in game.legal_moves(start) if m.end == end]
    assert options, f"no legal move {start} -> {end}"
    return next((m for m in options if m.promotion in (None, "Q")), options[0])


def _play(game: Game, start, end) -> None:
    assert game.move(_find(game, start, end)), f"move rejected: {start} -> {end}"


def test_opening_move_counts():
    game = Game()
    # 16 pawn moves (2 each) + 4 knight moves at the start.
    assert len(game.board.all_legal_moves(Color.WHITE)) == 20


def test_scholars_mate():
    game = Game()
    _play(game, (6, 4), (4, 4))  # 1. e4
    _play(game, (1, 4), (3, 4))  # 1... e5
    _play(game, (7, 5), (4, 2))  # 2. Bc4
    _play(game, (0, 1), (2, 2))  # 2... Nc6
    _play(game, (7, 3), (3, 7))  # 3. Qh5
    _play(game, (0, 6), (2, 5))  # 3... Nf6??
    _play(game, (3, 7), (1, 5))  # 4. Qxf7#

    assert game.status is GameStatus.CHECKMATE
    assert game.winner is Color.WHITE


def test_castling_available_when_path_is_clear():
    game = Game()
    _play(game, (6, 4), (4, 4))  # e4
    _play(game, (1, 4), (3, 4))  # e5
    _play(game, (7, 6), (5, 5))  # Nf3
    _play(game, (0, 6), (2, 5))  # Nf6
    _play(game, (7, 5), (4, 2))  # Bc4
    _play(game, (0, 5), (3, 2))  # Bc5
    # White can now castle king-side: king e1 -> g1.
    castles = [m for m in game.legal_moves((7, 4)) if m.is_castle]
    assert any(m.end == (7, 6) for m in castles)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all chess tests passed")
