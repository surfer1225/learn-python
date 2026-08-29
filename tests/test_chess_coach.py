"""Tests for the opening coach: SAN translation and book integrity.

Run from the project root:
    PYTHONPATH=. python tests/test_chess_coach.py
    # or
    python -m pytest tests/test_chess_coach.py
"""

import random

from chess import Color, Game, GameStatus

from chess_coach import book as book_mod
from chess_coach.coach import selftest
from chess_coach.san import from_san, normalize, play_san, replay, to_san


# --- SAN rendering ---------------------------------------------------------
def test_pawn_and_piece_moves():
    game = Game()
    assert to_san(game, from_san(game, "e4")) == "e4"
    assert to_san(game, from_san(game, "Nf3")) == "Nf3"


def test_capture_notation_uses_source_file_for_pawns():
    game = replay(["e4", "d5"])
    assert to_san(game, from_san(game, "exd5")) == "exd5"


def test_castling_both_sides():
    game = replay(["e4", "e5", "Nf3", "Nf6", "Bc4", "Bc5"])
    assert to_san(game, from_san(game, "O-O")) == "O-O"
    # Queen-side needs the b1/c1/d1 squares cleared first.
    game = replay(["d4", "d5", "Nc3", "Nc6", "Bf4", "Bf5", "Qd2", "Qd7"])
    assert to_san(game, from_san(game, "O-O-O")) == "O-O-O"


def test_check_and_mate_suffixes():
    # Scholar's Mate: the final move must render as '#', not '+'.
    game = replay(["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6"])
    mate = from_san(game, "Qxf7")
    assert to_san(game, mate) == "Qxf7#"
    game.move(mate)
    assert game.status is GameStatus.CHECKMATE

    # A plain check.
    game = replay(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "c3", "Nf6", "d4", "exd4", "cxd4"])
    assert to_san(game, from_san(game, "Bb4")) == "Bb4+"


def test_disambiguation_by_file():
    # Italian main line: both knights (b1 and f3) can recapture on d2.
    game = replay(
        ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "c3", "Nf6",
         "d4", "exd4", "cxd4", "Bb4+", "Bd2", "Bxd2+"]
    )
    options = {to_san(game, m) for m in game.board.all_legal_moves(Color.WHITE) if m.end == (6, 3)}
    assert options == {"Nbxd2", "Nfxd2", "Qxd2", "Kxd2"}


def test_promotion_notation():
    # White's pawn walks d5-d6xc7 and promotes on the eighth rank.
    game = replay(["e4", "d5", "exd5", "Nf6", "d6", "e5", "dxc7", "Be7"])
    c7 = (1, 2)
    promotions = {to_san(game, m) for m in game.board.all_legal_moves(Color.WHITE) if m.start == c7}
    assert "cxb8=Q" in promotions  # takes the knight, no check
    assert "cxd8=Q+" in promotions  # takes the queen, checks the king on e8
    assert "cxb8=N" in promotions  # underpromotion is a distinct move
    # c8 is blocked by Black's bishop, so there is no quiet promotion.
    assert not any(p.startswith("c8") for p in promotions)


# --- SAN parsing -----------------------------------------------------------
def test_parsing_is_lenient_about_noise():
    game = replay(["e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6"])
    for spelling in ("Qxf7#", "Qxf7", "Qxf7+", " Qxf7 ", "Qf7"):
        assert from_san(game, spelling) is not None, spelling
    # Case still matters: 'q' is not the queen, and there is no q-file.
    assert from_san(game, "qxf7") is None


def test_castling_accepts_zeroes():
    game = replay(["e4", "e5", "Nf3", "Nf6", "Bc4", "Bc5"])
    assert from_san(game, "0-0") == from_san(game, "O-O")


def test_illegal_and_nonsense_moves_return_none():
    game = Game()
    assert from_san(game, "e5") is None  # two squares is e4, not e5, on move one
    assert from_san(game, "Ke2") is None  # blocked
    assert from_san(game, "zz9") is None
    assert from_san(game, "") is None


def test_san_is_a_bijection_on_random_games():
    """The property everything else rests on.

    `from_san` works by rendering every legal move and matching the string, so
    it is correct exactly when SAN is injective over the legal moves of a
    position. Test that directly — rendering all moves once per position —
    rather than calling `from_san` per move, which would be quadratic.
    """
    rng = random.Random(0)
    positions = 0
    for _ in range(12):
        game = Game()
        for _ply in range(20):
            moves = game.board.all_legal_moves(game.turn)
            if not moves:
                break
            rendered = [normalize(to_san(game, m)) for m in moves]
            assert len(set(rendered)) == len(rendered), (
                f"two legal moves share a SAN: "
                f"{[s for s in rendered if rendered.count(s) > 1]}"
            )
            # Spot-check the parse direction on a sample (from_san is the
            # expensive call, so a few per position rather than all).
            for move in rng.sample(moves, min(3, len(moves))):
                san = to_san(game, move)
                assert from_san(game, san) == move, f"{san} did not round-trip"
            positions += 1
            game.move(rng.choice(moves))
    assert positions > 200, f"only covered {positions} positions"


# --- book integrity --------------------------------------------------------
def test_every_book_line_is_legal_and_canonical():
    assert selftest(verbose=False) == 0


def test_book_keys_are_unique_and_slug_like():
    keys = [line.key for line in book_mod.LINES]
    assert len(keys) == len(set(keys))
    assert all(k.isalnum() and k.islower() for k in keys)


def test_every_line_has_teaching_content():
    for line in book_mod.LINES:
        assert line.summary and line.plans, f"{line.key} has no summary/plans"
        for move in line.moves:
            assert move.idea.strip(), f"{line.key}: {move.san} has no idea"
            assert move.idea[0].isupper(), f"{line.key}: {move.san} idea not a sentence"


def test_matching_narrows_as_moves_are_played():
    assert len(book_mod.matching([])) == len(book_mod.LINES)
    after_e4 = book_mod.matching(["e4"])
    after_d4 = book_mod.matching(["d4"])
    assert after_e4 and after_d4
    assert not set(after_e4) & set(after_d4)
    # A move no line plays leaves the book entirely.
    assert book_mod.matching(["a4"]) == []


def test_next_moves_offers_book_continuations():
    options = book_mod.next_moves(["e4", "e5", "Nf3", "Nc6"])
    sans = {bm.san for _line, bm in options}
    assert {"Bc4", "Bb5", "d4"} <= sans


def test_hero_side_moves_land_on_the_right_ply():
    """A White repertoire must have the hero to move on even plies."""
    for line in book_mod.LINES:
        game = Game()
        for ply, book_move in enumerate(line.moves):
            expected = Color.WHITE if ply % 2 == 0 else Color.BLACK
            assert game.turn is expected, f"{line.key} ply {ply}"
            assert play_san(game, book_move.san) is not None


# --- gambits ---------------------------------------------------------------
def test_gambit_keys_unique_and_distinct_from_openings():
    keys = [g.key for g in gambits_mod.GAMBITS]
    assert len(keys) == len(set(keys))
    assert not set(keys) & set(book_mod.BY_KEY), "a gambit key shadows an opening key"


def test_every_gambit_line_is_legal_and_canonical():
    for gambit in gambits_mod.GAMBITS:
        game = Game()
        for ply, book_move in enumerate(gambit.moves, start=1):
            move = from_san(game, book_move.san)
            assert move is not None, f"{gambit.key} ply {ply}: illegal {book_move.san!r}"
            assert to_san(game, move) == book_move.san, f"{gambit.key} ply {ply}"
            game.move(move)


def test_sacrifice_ply_belongs_to_the_gambiteer():
    for gambit in gambits_mod.GAMBITS:
        assert 0 <= gambit.sacrifice_ply < len(gambit.moves), gambit.key
        mover = Color.WHITE if gambit.sacrifice_ply % 2 == 0 else Color.BLACK
        assert mover is gambit.hero, f"{gambit.key}: sacrifice is not the hero's move"


def test_gambiteer_actually_ends_up_down_material():
    """A gambit that costs nothing is not a gambit — except the Queen's,
    which is in the set precisely to make that point."""
    for gambit in gambits_mod.GAMBITS:
        final = _material_count(replay(gambit.sans))
        sign = 1 if gambit.hero is Color.WHITE else -1
        if gambit.soundness is gambits_mod.Soundness.NOT_A_GAMBIT:
            assert final == 0, f"{gambit.key} should end level, got {final:+d}"
        else:
            assert final * sign < 0, f"{gambit.key} is not down material ({final:+d})"


def test_stated_cost_matches_the_board():
    """The prose says 'one pawn' or 'two pawns'; the position must agree."""
    expected = {"evans": 1, "kingsgambit": 1, "danish": 2, "smithmorra": 1,
                "marshall": 1, "benko": 1, "budapest": 1, "englund": 1,
                "queensgambit": 0}
    for gambit in gambits_mod.GAMBITS:
        final = abs(_material_count(replay(gambit.sans)))
        assert final == expected[gambit.key], f"{gambit.key}: board says {final}"


def test_gambits_are_reachable_through_learn_and_drill():
    for gambit in gambits_mod.GAMBITS:
        line = resolve(gambit.key)
        assert line is not None and line.key == gambit.key
        assert line.plans, f"{gambit.key} exposes no plans via its Line view"


def test_every_gambit_has_the_teaching_fields():
    for gambit in gambits_mod.GAMBITS:
        assert gambit.compensation, gambit.key
        assert gambit.test.strip() and gambit.verdict.strip(), gambit.key
        assert gambit.cost.strip(), gambit.key


def test_soundness_spread_covers_the_range():
    """The set is meant to contrast good and bad sacrifices, not just list
    famous ones — if every entry were 'Sound' the mode would teach nothing."""
    present = {g.soundness for g in gambits_mod.GAMBITS}
    assert gambits_mod.Soundness.SOUND in present
    assert gambits_mod.Soundness.DUBIOUS in present
    assert gambits_mod.Soundness.NOT_A_GAMBIT in present
    assert len(present) >= 4


def test_show_gambit_renders_without_pausing():
    import contextlib
    import io

    for gambit in gambits_mod.GAMBITS:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            show_gambit(gambit, pause=False)
        out = buf.getvalue()
        assert "THE SACRIFICE" in out, gambit.key
        assert gambit.test[:20] in out, gambit.key
        assert "Material:" in out, gambit.key


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all chess_coach tests passed")
