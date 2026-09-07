"""The part of the coach that does not come out of the book.

`book.py` knows thirteen lines cold and has a sentence of reasoning for every
ply in them. That covers about two hundred positions. The other several million
are what this file is for: a language model that can answer "why is my move
worse than the book move", "what is the plan here", and "you have left the
book — now what", none of which can be written down in advance.

The rule it works under is the one the whole package already follows, applied
to a new source of claims: **the engine has the final say.** A model asked
about chess will, sooner or later, name a move that is not on the board, and it
will do so in confident prose. So no answer arrives as prose. Every reply is
JSON with three fields — the explanation, one recommended move, and one
variation — and the last two go through the engine before the learner sees
them:

* the move is looked up in the position's legal moves and re-rendered in the
  engine's own spelling, so `Nf3` typed for an impossible knight is dropped;
* the variation is replayed ply by ply from the current position and truncated
  at the first move that will not play.

What survives is checked; what does not survive is shown as having been
dropped, because "the coach suggested something impossible" is itself worth
knowing. The prose is printed as written — an opinion about a plan is not the
kind of claim an engine can adjudicate, and pretending otherwise would be its
own kind of dishonesty.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from chess.game import Game

from . import book as book_mod
from . import gambits as gambits_mod
from .llm import Config, LLMUnavailable, resolve
from .position import Snapshot
from .san import from_san, replay, to_san

# How hard the model should think, by task. Choosing a move in a sparring game
# happens every ply and wants to feel like an opponent rather than a wait;
# explaining a mistake happens on demand and is the whole reason the learner
# asked, so it gets more.
EFFORT = {"ask": "high", "critique": "high", "review": "high", "spar": "medium"}

# Three fields, all required. `move` and `line` are plain strings and a plain
# array rather than nullable types: "" and [] are unambiguous, and they keep
# the schema inside the subset every strict JSON-schema implementation agrees
# on.
ANSWER_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "answer": {
            "type": "string",
            "description": (
                "The coaching, in prose. At most 150 words. Plain text; wrap a "
                "phrase in *asterisks* for emphasis."
            ),
        },
        "move": {
            "type": "string",
            "description": (
                "The single move you recommend in the CURRENT position, in "
                "SAN, copied exactly from the legal move list you were given. "
                "Empty string if the question is not asking you to choose a "
                "move."
            ),
        },
        "line": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "A variation illustrating the point, as SAN plies starting "
                "from the CURRENT position and alternating sides. It will be "
                "replayed on the real board and cut at the first move that is "
                "not legal. Empty array if you are not showing a line."
            ),
        },
    },
    "required": ["answer", "move", "line"],
    "additionalProperties": False,
}


HOUSE_STYLE = """\
You are a chess coach embedded in a terminal trainer. The learner is looking at \
a board you cannot see, so you are given the position in FEN, the moves played \
so far, and the complete list of legal moves.

How to answer:

- Say what a move *achieves*, never what it does. "Nf3" does not need \
"develops the knight to f3" — they can see that. It needs "attacks e5, so Black \
has to answer instead of getting on with their own plan."
- One idea, made well, beats five listed. 150 words is the ceiling and most \
answers should be shorter.
- Name the pattern when there is one — fork, pin, back-rank, outpost, minority \
attack, bad bishop. A named pattern can be recalled in a future game; a \
description cannot.
- Concrete beats general. If a move loses a piece, give the sequence. If it is \
merely passive, say which of the opponent's plans it fails to stop.
- If the honest answer is "these are both fine and it is a matter of taste", \
say that. Do not manufacture an evaluation to sound useful, and do not soften \
a real mistake into a preference.
- You are talking to one person, out loud. No headings, no bullet lists, no \
markdown tables.

About moves specifically:

- Any move you name for the current position must be copied from the legal move \
list you were given. There are no exceptions to this and no move is worth \
guessing at.
- Put variations in the `line` field, not in the prose. They are replayed on the \
real board before the learner sees them, so a line that is right survives \
intact and a line that is wrong is visibly cut short.
- If you are not recommending a move, leave `move` empty. An empty field is a \
better answer than a move you are unsure of.\
"""


def repertoire_index() -> str:
    """The book, one line each, so the tutor can point back at it.

    The learner is working through a specific repertoire. An answer that ends
    "this is the same idea as the c3 push you drilled in the Italian" is worth
    several that do not, and the model cannot make that connection without
    knowing what is in the book. Cheap to include, and it sits inside the
    cached prefix.
    """
    lines = [
        "The learner's repertoire in this trainer, which you may refer to by name:"
    ]
    for line in book_mod.LINES:
        lines.append(f"  {line.key}: {line.name} [{line.eco}], as {line.hero.value}")
    lines.append("Gambits available to study:")
    for gambit in gambits_mod.GAMBITS:
        lines.append(
            f"  {gambit.key}: {gambit.name} [{gambit.eco}] — {gambit.soundness.value}"
        )
    return "\n".join(lines)


def system_prompt() -> str:
    return f"{HOUSE_STYLE}\n\n{repertoire_index()}"


# --- what comes back -------------------------------------------------------
@dataclass(frozen=True)
class Answer:
    """A reply that has been through the engine.

    `move` and `line` hold only what checked out. `dropped_move` and
    `cut_line_at` hold what did not, and are surfaced rather than swallowed:
    the learner is entitled to know when their coach said something impossible.
    """

    text: str
    move: Optional[str] = None
    line: Tuple[str, ...] = ()
    dropped_move: Optional[str] = None
    cut_line_at: Optional[str] = None

    @property
    def grounded(self) -> bool:
        return self.dropped_move is None and self.cut_line_at is None


class TutorUnavailable(LLMUnavailable):
    """Raised by every Tutor method when there is nothing to call."""


class Tutor:
    """The AI half of the coach.

    Holds a short conversation thread for `ask`, so follow-ups ("and if he
    takes?") work, and nothing at all for the other methods, which are
    one-shot by nature: a critique of one move should not be coloured by the
    critique of the last one.
    """

    # Enough for a real back-and-forth, short enough that the cached system
    # prefix stays the dominant part of the request.
    THREAD_LIMIT = 12

    def __init__(self, backend: Optional[Any] = None, *, config: Optional[Config] = None) -> None:
        self.reason: Optional[str] = None
        if backend is not None:
            self.backend = backend
        else:
            self.backend, self.reason = resolve(config)
        self._thread: List[Dict[str, Any]] = []

    @property
    def available(self) -> bool:
        return self.backend is not None

    def describe(self) -> str:
        if not self.available:
            return f"off — {self.reason}"
        return self.backend.config.describe()

    def forget(self) -> None:
        """Drop the conversation thread. Called when a new position is set up."""
        self._thread.clear()

    # --- the five things it is asked -------------------------------------
    def ask(
        self,
        snapshot: Snapshot,
        question: str,
        *,
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Answer:
        """A free question about the position on the board."""
        prompt = (
            f"{snapshot.brief()}\n\n"
            f"The learner asks: {question}\n\n"
            "Answer for this exact position."
        )
        return self._threaded(prompt, EFFORT["ask"], snapshot, on_progress)

    def critique(
        self,
        snapshot: Snapshot,
        played: str,
        better: str,
        idea: str,
        *,
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Answer:
        """Why the move they played is worse than the one the book plays.

        This is the gap the book cannot cover. It carries a refutation for
        every trap it knows about, but a learner's inferior move is usually not
        a trap — it is a reasonable-looking move that quietly concedes
        something, and there is no way to enumerate those in advance.

        The snapshot is the position *before* their move, so the legal list
        contains both moves and the model can compare them directly.
        """
        prompt = (
            f"{snapshot.brief()}\n\n"
            f"The learner played {played}. The book plays {better}, because: {idea}\n\n"
            f"{played} is legal but not the book move. Explain what {played} "
            f"concedes that {better} does not. Be specific about the position — "
            f"if {played} actually loses material, give the sequence in `line`. "
            f"If it is merely a shade worse, say so plainly rather than "
            f"inflating it. Set `move` to {better}."
        )
        return self._once(prompt, EFFORT["critique"], snapshot, on_progress)

    def deepen(
        self,
        snapshot: Snapshot,
        book_move: str,
        idea: str,
        *,
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Answer:
        """The book's one sentence, opened out.

        The book is deliberately terse — one sentence per ply, because a wall
        of prose in a drill is not read. This is the escape hatch for the ply
        where the one sentence was not enough.
        """
        prompt = (
            f"{snapshot.brief()}\n\n"
            f"The book plays {book_move} here, and says: {idea}\n\n"
            "Go one level deeper than that sentence. What is the plan behind "
            "the move over the next few moves, and what would go wrong without "
            f"it? Set `move` to {book_move} and use `line` to show the plan if "
            "it helps."
        )
        return self._once(prompt, EFFORT["ask"], snapshot, on_progress)

    def review(
        self,
        snapshot: Snapshot,
        *,
        note: str = "",
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Answer:
        """A verdict on the whole game so far, not on one move."""
        prompt = (
            f"{snapshot.brief()}\n\n"
            + (f"{note}\n\n" if note else "")
            + "Review the game to this point. Name the single most useful thing "
            "the learner should take away — the recurring habit, not a list of "
            "individual moves. If the play was sound, say so and name what "
            "they got right. Leave `move` empty unless there is one move worth "
            "singling out."
        )
        return self._once(prompt, EFFORT["review"], snapshot, on_progress)

    def spar(
        self,
        snapshot: Snapshot,
        *,
        learner_move: Optional[str] = None,
        level: str = "club",
        on_progress: Optional[Callable[[], None]] = None,
    ) -> Answer:
        """One ply of a sparring game: a word on their move, then a reply.

        Both halves come from a single request. Two requests per ply would
        double the cost and the wait to buy a separation the learner never
        sees, and the assessment is better for being written by the same pass
        that had to find a move.
        """
        strength = STRENGTHS.get(level, STRENGTHS["club"])
        opening = (
            f"The learner just played {learner_move}. In one or two sentences, "
            "say whether it was a good move and why."
            if learner_move
            else "This is your first move of the game. Introduce your choice in "
            "one sentence."
        )
        prompt = (
            f"{snapshot.brief()}\n\n"
            f"You are playing this game against the learner as {snapshot.to_move}. "
            f"{strength}\n\n"
            f"{opening} Then set `move` to your reply, copied from the legal "
            "move list. Never play a move you could not explain."
        )
        return self._once(prompt, EFFORT["spar"], snapshot, on_progress)

    # --- plumbing ---------------------------------------------------------
    def _threaded(
        self,
        prompt: str,
        effort: str,
        snapshot: Snapshot,
        on_progress: Optional[Callable[[], None]],
    ) -> Answer:
        self._thread.append({"role": "user", "content": prompt})
        reply = self._call(self._thread, effort, on_progress)
        # Only the prose goes back into the thread. Re-sending the JSON would
        # teach the model that its own unvalidated moves are part of the
        # record, which is the opposite of what this file is for.
        self._thread.append(
            {"role": "assistant", "content": reply.get("answer", "") or "(no answer)"}
        )
        del self._thread[: max(0, len(self._thread) - self.THREAD_LIMIT)]
        return ground(reply, snapshot)

    def _once(
        self,
        prompt: str,
        effort: str,
        snapshot: Snapshot,
        on_progress: Optional[Callable[[], None]],
    ) -> Answer:
        return ground(
            self._call([{"role": "user", "content": prompt}], effort, on_progress),
            snapshot,
        )

    def _call(
        self,
        messages: Sequence[Dict[str, Any]],
        effort: str,
        on_progress: Optional[Callable[[], None]],
    ) -> Dict[str, Any]:
        if self.backend is None:
            raise TutorUnavailable(self.reason or "No model configured.")
        return self.backend.ask_json(
            system=system_prompt(),
            messages=messages,
            schema=ANSWER_SCHEMA,
            effort=effort,
            on_progress=on_progress,
        )


STRENGTHS = {
    "beginner": (
        "Play like a careful beginner: sound developing moves, no traps, and "
        "take material only when it is free."
    ),
    "club": (
        "Play like a solid club player: principled moves, punish real mistakes, "
        "but do not play the sharpest computer line if a clear human one exists."
    ),
    "strong": (
        "Play the strongest move you can find, and say so when the position "
        "turns against the learner."
    ),
}


# --- grounding -------------------------------------------------------------
def ground(reply: Dict[str, Any], snapshot: Snapshot) -> Answer:
    """Turn a raw JSON reply into an `Answer` the engine has vouched for."""
    game = _position(snapshot)
    text = str(reply.get("answer") or "").strip()

    raw_move = str(reply.get("move") or "").strip()
    move = canonical(game, raw_move) if raw_move else None
    dropped = raw_move if (raw_move and move is None) else None

    raw_line = reply.get("line") or []
    if not isinstance(raw_line, list):
        raw_line = []
    line, cut = walk(snapshot, [str(m) for m in raw_line])

    return Answer(
        text=text, move=move, line=line, dropped_move=dropped, cut_line_at=cut
    )


def canonical(game: Game, san: str) -> Optional[str]:
    """The engine's own spelling of `san`, or None if it will not play.

    Going through `from_san` and back out through `to_san` does two jobs at
    once: it rejects the impossible, and it normalises what is left. A model
    that writes `Nbd2` where the engine writes `Nd2` — or omits a check mark
    the engine includes — should not produce a move that looks different from
    every other move on screen.
    """
    move = from_san(game, san)
    return to_san(game, move) if move is not None else None


def walk(snapshot: Snapshot, sans: Sequence[str]) -> Tuple[Tuple[str, ...], Optional[str]]:
    """Replay a suggested variation, stopping at the first move that will not play.

    Returns the prefix that was legal and the move that ended it. This is the
    same replay the book's `--selftest` runs, pointed at model output instead
    of at hand-written data — which is the right shape for it, since the model
    is exactly as capable of a typo and rather more prolific.
    """
    game = _position(snapshot)
    played: List[str] = []
    for san in sans:
        move = from_san(game, san)
        if move is None:
            return tuple(played), san
        played.append(to_san(game, move))
        game.move(move)
    return tuple(played), None


def _position(snapshot: Snapshot) -> Game:
    """A private board at the snapshot's position.

    Replayed from the move history rather than handed a reference to the live
    game, so that walking a hypothetical variation can never disturb the
    position the learner is actually looking at.
    """
    return replay(list(snapshot.history))
