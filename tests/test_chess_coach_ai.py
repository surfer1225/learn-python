"""Tests for the AI coach: position description, and the grounding of replies.

None of these touch the network. `FakeBackend` presents the same surface as the
real one, so the prompt that gets built and the checking that happens to the
reply are exercised exactly as they run against the live model — which is the
only part worth testing, since what the model *says* is not ours to assert.

Run from the project root:
    PYTHONPATH=. python tests/test_chess_coach_ai.py
    # or
    python -m pytest tests/test_chess_coach_ai.py
"""

import contextlib
import io

from chess.game import Game

from chess_coach import book as book_mod
from chess_coach.coach import _show_answer
from chess_coach.llm import Config, FakeBackend, LLMUnavailable
from chess_coach.position import (
    Snapshot,
    fen,
    halfmove_clock,
    legal_sans,
    material_phrase,
)
from chess_coach.render import movelist
from chess_coach.san import replay
from chess_coach.tutor import (
    ANSWER_SCHEMA,
    Answer,
    Tutor,
    TutorUnavailable,
    canonical,
    ground,
    system_prompt,
    walk,
)

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def snapshot(sans, **kwargs):
    return Snapshot.of(replay(list(sans)), list(sans), **kwargs)


# --- FEN -------------------------------------------------------------------
def test_start_position_fen_is_the_standard_one():
    assert fen(Game()) == START_FEN


def test_double_pawn_push_sets_the_en_passant_square():
    # The square the pawn skipped, not the square it landed on.
    assert fen(replay(["e4"]), ["e4"]).split()[3] == "e3"
    assert fen(replay(["e4", "e5"]), ["e4", "e5"]).split()[3] == "e6"
    # A knight move clears it again.
    moves = ["e4", "e5", "Nf3"]
    assert fen(replay(moves), moves).split()[3] == "-"


def test_castling_rights_come_off_as_the_pieces_move():
    moves = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "O-O"]
    assert fen(replay(moves), moves).split()[2] == "kq"
    # Moving a rook costs one side only.
    rook = ["a4", "a5", "Ra3"]
    assert fen(replay(rook), rook).split()[2] == "Kkq"


def test_move_counters_come_from_the_history():
    moves = ["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "O-O"]
    _, _, _, _, halfmove, fullmove = fen(replay(moves), moves).split()
    assert (halfmove, fullmove) == ("5", "4")  # last pawn move was 1...e5
    # A capture resets the clock.
    captures = ["e4", "d5", "exd5"]
    assert fen(replay(captures), captures).split()[4] == "0"


def test_halfmove_clock_reads_pawn_moves_and_captures_off_the_san():
    assert halfmove_clock([]) == 0
    assert halfmove_clock(["e4"]) == 0
    assert halfmove_clock(["e4", "Nf6", "Nc3"]) == 2
    assert halfmove_clock(["e4", "d5", "exd5", "Nf6", "Nc3"]) == 2


def test_material_phrase_names_the_leader():
    assert material_phrase(Game().board) == "level"
    down_a_pawn = replay(["e4", "d5", "exd5"])
    assert material_phrase(down_a_pawn.board) == "White +1 (pawn)"


# --- what the model is told ------------------------------------------------
def test_legal_sans_matches_the_engine_exactly():
    game = replay(["e4", "e5", "Nf3"])
    assert len(legal_sans(game)) == len(game.board.all_legal_moves(game.turn))
    assert legal_sans(game) == sorted(legal_sans(game))  # stable for the cache


def test_brief_carries_everything_an_answer_could_need():
    snap = snapshot(["e4", "e5", "Nf3"], studying="Italian Game")
    text = snap.brief()
    assert snap.fen in text
    assert "1. e4 e5  2. Nf3" in text
    assert "To move: black" in text
    assert "Italian Game" in text
    # The legal move list is the whole point: without it a recommendation is a
    # guess, and there is nothing to check it against.
    for san in snap.legal:
        assert san in text


def test_brief_says_so_at_the_starting_position():
    assert "starting position" in snapshot([]).brief()


def test_system_prompt_names_the_repertoire_and_forbids_invented_moves():
    prompt = system_prompt()
    for line in book_mod.LINES:
        assert line.key in prompt, line.key
    assert "copied from the legal move list" in prompt
    assert "achieves" in prompt  # the house style the book itself follows


def test_answer_schema_is_closed_and_fully_required():
    assert ANSWER_SCHEMA["additionalProperties"] is False
    assert set(ANSWER_SCHEMA["required"]) == set(ANSWER_SCHEMA["properties"])


# --- grounding: the point of the whole exercise ----------------------------
def test_a_legal_move_survives_and_is_respelled_by_the_engine():
    snap = snapshot(["e4", "e5", "Nf3", "Nc6"])
    answer = ground({"answer": "Take the diagonal.", "move": "Bc4", "line": []}, snap)
    assert answer.move == "Bc4"
    assert answer.dropped_move is None
    assert answer.grounded
    # Sloppy spelling is normalised rather than rejected: 'ed5' is what a
    # learner types for 'exd5', and a model is no more careful.
    after = snapshot(["e4", "d5"])
    assert ground({"answer": "", "move": "ed5", "line": []}, after).move == "exd5"


def test_an_impossible_move_is_dropped_and_reported():
    snap = snapshot(["e4", "e5"])
    answer = ground({"answer": "Play this.", "move": "Nf6", "line": []}, snap)
    assert answer.move is None
    assert answer.dropped_move == "Nf6"  # it is White to move
    assert not answer.grounded
    # The prose still gets through — an opinion about a plan is not a claim the
    # engine is entitled to veto.
    assert answer.text == "Play this."


def test_nonsense_in_the_move_field_does_not_reach_the_learner():
    snap = snapshot([])
    for junk in ("Qxz9", "the knight move", "1. e4", "!!"):
        assert ground({"answer": "", "move": junk, "line": []}, snap).move is None


def test_an_empty_move_field_is_not_a_dropped_move():
    answer = ground({"answer": "Both are fine.", "move": "", "line": []}, snapshot([]))
    assert answer.move is None and answer.dropped_move is None
    assert answer.grounded


def test_a_legal_variation_is_kept_whole():
    snap = snapshot(["e4", "e5"])
    line, cut = walk(snap, ["Nf3", "Nc6", "Bb5"])
    assert line == ("Nf3", "Nc6", "Bb5")
    assert cut is None


def test_a_variation_is_cut_at_the_first_move_that_will_not_play():
    snap = snapshot(["e4", "e5"])
    line, cut = walk(snap, ["Nf3", "Nc6", "Qxf7"])  # the queen cannot get there
    assert line == ("Nf3", "Nc6")
    assert cut == "Qxf7"


def test_a_variation_is_respelled_and_check_marks_restored():
    """Scholar's mate: the model writes 'Qxf7', the engine writes 'Qxf7#'."""
    snap = snapshot(["e4", "e5", "Bc4", "Nc6"])
    line, cut = walk(snap, ["Qh5", "Nf6", "Qxf7"])
    assert line == ("Qh5", "Nf6", "Qxf7#")
    assert cut is None


def test_walking_a_variation_does_not_disturb_the_real_position():
    snap = snapshot(["e4", "e5"])
    walk(snap, ["Nf3", "Nc6", "Bb5"])
    assert snap.fen == fen(replay(list(snap.history)), snap.history)
    assert snap.history == ("e4", "e5")


def test_canonical_rejects_a_move_from_the_wrong_side():
    game = replay(["e4"])  # Black to move
    assert canonical(game, "Nf3") is None
    assert canonical(game, "Nf6") == "Nf6"


# --- the tutor end to end (against the fake backend) -----------------------
def test_ask_sends_the_position_and_grounds_the_reply():
    backend = FakeBackend([{"answer": "Take the centre.", "move": "e4", "line": ["e4", "e5"]}])
    tutor = Tutor(backend)
    snap = snapshot([])
    answer = tutor.ask(snap, "what should I open with?")

    call = backend.calls[0]
    assert snap.fen in call["messages"][0]["content"]
    assert "what should I open with?" in call["messages"][0]["content"]
    assert call["schema"] is ANSWER_SCHEMA
    assert answer.move == "e4" and answer.line == ("e4", "e5")


def test_critique_puts_both_moves_in_front_of_the_model():
    backend = FakeBackend([{"answer": "It blocks the c-pawn.", "move": "c3", "line": []}])
    snap = snapshot(["e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5"])
    Tutor(backend).critique(snap, "Nc3", "c3", "It prepares d4.")
    prompt = backend.calls[0]["messages"][0]["content"]
    assert "The learner played Nc3" in prompt
    assert "The book plays c3" in prompt
    assert "It prepares d4." in prompt


def test_ask_remembers_the_thread_but_only_the_prose():
    backend = FakeBackend(
        [
            {"answer": "Because it holds e5.", "move": "Nc6", "line": []},
            {"answer": "Then you are fine.", "move": "", "line": []},
        ]
    )
    tutor = Tutor(backend)
    snap = snapshot(["e4", "e5", "Nf3"])
    tutor.ask(snap, "why Nc6?")
    tutor.ask(snap, "and if he takes?")

    thread = backend.calls[1]["messages"]
    assert [m["role"] for m in thread] == ["user", "assistant", "user"]
    # The assistant turn is the prose only. Feeding the JSON back would put the
    # model's unchecked moves into the record as if they had been accepted.
    assert thread[1]["content"] == "Because it holds e5."
    assert "Nc6" not in thread[1]["content"]


def test_one_shot_calls_do_not_share_the_thread():
    backend = FakeBackend([{"answer": "a", "move": "", "line": []}] * 2)
    tutor = Tutor(backend)
    snap = snapshot(["e4"])
    tutor.deepen(snap, "e5", "Stakes an equal claim.")
    tutor.review(snap)
    assert all(len(call["messages"]) == 1 for call in backend.calls)


def test_forget_clears_the_thread():
    backend = FakeBackend([{"answer": "a", "move": "", "line": []}] * 2)
    tutor = Tutor(backend)
    tutor.ask(snapshot([]), "one")
    tutor.forget()
    tutor.ask(snapshot([]), "two")
    assert len(backend.calls[1]["messages"]) == 1


def test_the_thread_is_bounded():
    replies = [{"answer": "x", "move": "", "line": []} for _ in range(20)]
    backend = FakeBackend(replies)
    tutor = Tutor(backend)
    for i in range(20):
        tutor.ask(snapshot([]), f"question {i}")
    assert len(backend.calls[-1]["messages"]) <= Tutor.THREAD_LIMIT


def test_spar_asks_for_an_assessment_and_a_reply_in_one_call():
    backend = FakeBackend([{"answer": "Natural.", "move": "e5", "line": []}])
    snap = snapshot(["e4"])
    answer = Tutor(backend).spar(snap, learner_move="e4", level="strong")
    prompt = backend.calls[0]["messages"][0]["content"]
    assert "The learner just played e4" in prompt
    assert "strongest move" in prompt  # the 'strong' strength description
    assert answer.move == "e5"
    assert len(backend.calls) == 1


def test_spar_opens_the_game_when_there_is_no_move_to_comment_on():
    backend = FakeBackend([{"answer": "I like the centre.", "move": "e4", "line": []}])
    Tutor(backend).spar(snapshot([]), learner_move=None)
    assert "first move of the game" in backend.calls[0]["messages"][0]["content"]


def test_effort_is_lower_for_sparring_than_for_explaining():
    backend = FakeBackend([{"answer": "a", "move": "", "line": []}] * 2)
    tutor = Tutor(backend)
    tutor.spar(snapshot([]))
    tutor.ask(snapshot([]), "why?")
    assert backend.calls[0]["effort"] != backend.calls[1]["effort"]


# --- degrading without credentials -----------------------------------------
def test_no_credentials_is_a_reason_not_an_exception():
    tutor = Tutor(env={})
    assert not tutor.available
    assert "ANTHROPIC_API_KEY" in (tutor.reason or "")
    assert "off" in tutor.describe()


def test_calling_an_unavailable_tutor_raises_with_the_reason():
    tutor = Tutor(env={})
    try:
        tutor.ask(snapshot([]), "anything")
    except TutorUnavailable as exc:
        assert "ANTHROPIC_API_KEY" in str(exc)
    else:  # pragma: no cover - the call must not silently succeed
        raise AssertionError("an unavailable tutor answered a question")


def test_a_backend_failure_is_an_llm_unavailable():
    tutor = Tutor(FakeBackend([]))  # no scripted replies left
    try:
        tutor.ask(snapshot([]), "anything")
    except LLMUnavailable:
        pass
    else:  # pragma: no cover
        raise AssertionError("an exhausted backend did not report itself")


# --- configuration ---------------------------------------------------------
def test_vertex_is_chosen_when_a_project_is_set_and_no_key_is():
    config = Config.from_env(
        {"ANTHROPIC_VERTEX_PROJECT_ID": "proj", "CLOUD_ML_REGION": "us-east5"}
    )
    assert config.provider == "vertex"
    assert config.region == "us-east5"
    assert config.missing({}) is None  # a project is all Vertex needs here


def test_an_explicit_key_wins_over_a_vertex_project():
    env = {"ANTHROPIC_VERTEX_PROJECT_ID": "proj", "ANTHROPIC_API_KEY": "sk-test"}
    config = Config.from_env(env)
    assert config.provider == "anthropic"
    assert config.missing(env) is None


def test_the_provider_can_be_forced():
    env = {"CHESS_COACH_PROVIDER": "vertex", "ANTHROPIC_API_KEY": "sk-test"}
    assert Config.from_env(env).provider == "vertex"


def test_the_model_is_opus_unless_overridden():
    assert Config.from_env({}).model == "claude-opus-5"
    assert Config.from_env({"CHESS_COACH_MODEL": "claude-sonnet-5"}).model == "claude-sonnet-5"


def test_describe_names_the_model_and_where_it_lives():
    assert "Vertex" in Config(provider="vertex", model="m").describe()
    assert "Anthropic API" in Config(provider="anthropic", model="m").describe()


# --- rendering -------------------------------------------------------------
def test_a_variation_is_numbered_from_where_it_starts():
    assert movelist(["Nf3", "Nc6"], start=4) == "4. Nf3 Nc6"
    assert movelist(["Nc6", "Bb5"], start=3, black_first=True) == "3... Nc6  4. Bb5"
    assert movelist(["e4", "e5"]) == "1. e4 e5"  # the old behaviour is unchanged


def test_show_answer_prints_the_move_the_line_and_what_was_dropped():
    snap = snapshot(["e4", "e5"])
    answer = Answer(
        text="A thought.",
        move="Nf3",
        line=("Nf3", "Nc6"),
        dropped_move="Qh9",
        cut_line_at="Bxz3",
    )
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _show_answer(answer, snap)
    out = buf.getvalue()
    assert "A thought." in out
    assert "Nf3" in out
    assert "dropped Qh9" in out
    assert "cut at Bxz3" in out


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all chess_coach AI tests passed")
