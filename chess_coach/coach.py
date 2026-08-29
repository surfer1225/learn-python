"""The coach: three ways to work on an opening, plus a headless self-check.

    learn <key>    walk the line move by move, with the reasoning
    drill <key>    you play your side from memory; the coach answers and corrects
    explore        free play from the start; the coach names what you are in

`drill` is the mode that actually builds the skill. Reading a line teaches you
to recognise it; being asked for the move with nothing on screen but the board
teaches you to find it.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional

from chess.constants import Color
from chess.game import Game

from . import book as book_mod
from .book import PRINCIPLES, BookMove, Line
from .render import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RED,
    YELLOW,
    board_text,
    emphasize,
    movelist,
    paint,
    wrap,
)
from .san import from_san, normalize, play_san, to_san

BULLET = "  - "


@dataclass
class Session:
    """A game in progress plus the SAN history, which is what the book indexes on."""

    game: Game = field(default_factory=Game)
    played: List[str] = field(default_factory=list)
    last_move: Optional[object] = None

    def push(self, san: str) -> bool:
        move = from_san(self.game, san)
        if move is None:
            return False
        rendered = to_san(self.game, move)  # canonical form, before the board changes
        self.game.move(move)
        self.played.append(rendered)
        self.last_move = move
        return True

    @property
    def turn(self) -> Color:
        return self.game.turn


# --- output helpers --------------------------------------------------------
def _show_board(session: Session, flipped: bool, hint=None) -> None:
    squares = [session.last_move.start, session.last_move.end] if session.last_move else []
    print()
    print(board_text(session.game.board, flipped=flipped, highlight=squares, hint=hint))
    print()


def _say(text: str) -> None:
    print(emphasize(wrap(text, indent="   ")))


def _respond(label: str, text: str, *codes: str) -> None:
    """A coloured label followed by wrapped prose.

    Wrapping happens on the plain string — measuring width after adding ANSI
    escapes would count invisible characters and wrap far too early.
    """
    body = wrap(f"{label} {text}", indent="   ")
    if codes:
        body = body.replace(label, paint(label, *codes), 1)
    print(emphasize(body))


def _heading(text: str) -> None:
    print(paint(text, BOLD, CYAN))


def _describe(line: Line) -> None:
    _heading(f"\n{line.name}  [{line.eco}]")
    print(f"   Playing as: {paint(line.hero.value.title(), BOLD)}")
    print()
    _say(line.summary)


def _show_plans(line: Line) -> None:
    if not line.plans:
        return
    print(paint("\n   Plans from here:", BOLD))
    for plan in line.plans:
        body = wrap(f"- {plan}", indent="     ")
        print(emphasize(body))


def _show_traps(move: BookMove) -> None:
    for wrong, why in move.mistakes:
        body = wrap(f"{wrong} — {why}", indent="     ")
        print(emphasize(body.replace(wrong, paint(wrong, RED), 1)))


# --- learn -----------------------------------------------------------------
def learn(line: Line, *, pause: bool = True) -> None:
    """Walk the whole line, explaining each move."""
    _describe(line)
    session = Session()
    flipped = line.hero is Color.BLACK

    for ply, book_move in enumerate(line.moves):
        mover = Color.WHITE if ply % 2 == 0 else Color.BLACK
        number = ply // 2 + 1
        prefix = f"{number}." if mover is Color.WHITE else f"{number}..."
        tag = paint("you", GREEN) if mover is line.hero else paint("opponent", DIM)

        if not session.push(book_move.san):
            raise ValueError(f"{line.key}: illegal book move {book_move.san!r} at ply {ply + 1}")

        _show_board(session, flipped)
        print(f"   {paint(prefix + ' ' + book_move.san, BOLD)}   ({tag})")
        _say(book_move.idea)
        if book_move.mistakes:
            print(paint("\n   Instead:", DIM))
            _show_traps(book_move)

        if pause and ply < len(line.moves) - 1:
            try:
                if input(paint("\n   [enter] next, 'q' to stop  ", DIM)).strip().lower() == "q":
                    return
            except EOFError:
                return

    print(paint("\n   Line complete: ", BOLD) + movelist(session.played))
    _show_plans(line)


# --- drill -----------------------------------------------------------------
def drill(line: Line) -> None:
    """The learner plays the hero side; the coach replies from the book."""
    _describe(line)
    print()
    _say(
        "I will play the other side. Give me your move in algebraic notation "
        "(e4, Nf3, O-O, exd5). Type 'hint' for a nudge, 'idea' for the reason "
        "behind the last move, or 'quit' to stop."
    )

    session = Session()
    flipped = line.hero is Color.BLACK
    wrong_here = 0
    mistakes_made = 0

    ply = 0
    while ply < len(line.moves):
        book_move = line.moves[ply]
        mover = Color.WHITE if ply % 2 == 0 else Color.BLACK
        number = ply // 2 + 1

        if mover is not line.hero:
            session.push(book_move.san)
            _show_board(session, flipped)
            prefix = f"{number}." if mover is Color.WHITE else f"{number}..."
            print(f"   I play {paint(prefix + ' ' + book_move.san, BOLD)}")
            _say(book_move.idea)
            ply += 1
            continue

        _show_board(session, flipped)
        prompt = f"   {number}{'.' if mover is Color.WHITE else '...'} your move: "
        try:
            answer = input(paint(prompt, BOLD)).strip()
        except EOFError:
            print()
            return

        if not answer:
            continue
        low = answer.lower()
        if low in ("quit", "q", "exit"):
            return
        if low == "hint":
            print(f"   {paint('Hint:', YELLOW)} {_hint_for(book_move)}")
            continue
        if low == "idea":
            previous = line.moves[ply - 1] if ply else None
            print(f"   {previous.idea if previous else 'Nothing played yet.'}")
            continue

        if normalize(answer) == normalize(book_move.san):
            session.push(book_move.san)
            praise = "Correct." if wrong_here == 0 else "Right, that's the one."
            _respond(praise, book_move.idea, GREEN)
            wrong_here = 0
            ply += 1
            continue

        # Wrong. Three grades of wrong, and they deserve different answers:
        # a known trap gets its refutation, a merely-inferior move gets the
        # book move and moves on, and a typo gets nothing but a nudge.
        mistakes_made += 1
        wrong_here += 1
        known = _known_mistake(book_move, answer)
        if known is not None:
            _respond("No.", known, RED)
        elif from_san(session.game, answer) is not None:
            _respond(
                "Legal, but not the book move.",
                f"The move is {book_move.san} — {book_move.idea}",
                YELLOW,
            )
            session.push(book_move.san)
            ply += 1
            wrong_here = 0
            continue
        else:
            _respond("Not a legal move here.", "Check the notation and the board.", RED)
            mistakes_made -= 1  # a typo is not a chess error
            wrong_here -= 1

        if wrong_here >= 2:
            _respond("The move is", f"{book_move.san} — {book_move.idea}", BOLD)
            session.push(book_move.san)
            ply += 1
            wrong_here = 0

    _show_board(session, flipped)
    score = "clean run — nothing to correct" if mistakes_made == 0 else f"{mistakes_made} correction(s)"
    print(paint(f"   Line complete: {score}.", BOLD))
    print("   " + movelist(session.played))
    _show_plans(line)


def _hint_for(book_move: BookMove) -> str:
    """A nudge that does not give the move away: the piece and the idea."""
    san = book_move.san
    if san.startswith("O-O"):
        return "Think about king safety."
    names = {"K": "king", "Q": "queen", "R": "rook", "B": "bishop", "N": "knight"}
    if san[0] in names:
        return f"Move the {names[san[0]]}. {book_move.idea.split('.')[0]}."
    return f"It's a pawn move. {book_move.idea.split('.')[0]}."


def _known_mistake(book_move: BookMove, answer: str) -> Optional[str]:
    for wrong, why in book_move.mistakes:
        if normalize(wrong) == normalize(answer):
            return why
    return None


# --- gambits ---------------------------------------------------------------
def show_gambit(gambit: Gambit, *, pause: bool = True) -> None:
    """Play a gambit out, stopping at the sacrifice to show the trade.

    The board is drawn twice at the critical moment — once before the offer
    with the square marked, once after — because the whole idea is easier to
    see as a before/after than as a sentence.
    """
    _heading(f"\n{gambit.name}  [{gambit.eco}]")
    print(
        f"   {paint(gambit.soundness.value, _soundness_colour(gambit.soundness))}"
        f" · {paint(gambit.hero.value.title(), BOLD)}"
    )
    _say(gambit.soundness.blurb)

    print(paint("\n   You give:", BOLD) + f"  {gambit.cost}")
    print(paint("   You get:", BOLD))
    for item in gambit.compensation:
        print(emphasize(wrap(f"- {item}", indent="     ")))

    session = Session()
    flipped = gambit.hero is Color.BLACK

    for ply, book_move in enumerate(gambit.moves):
        mover = Color.WHITE if ply % 2 == 0 else Color.BLACK
        prefix = f"{ply // 2 + 1}." if mover is Color.WHITE else f"{ply // 2 + 1}..."
        is_sac = ply == gambit.sacrifice_ply

        if is_sac:
            # Mark the square the pawn is about to step onto, before it moves.
            offered = from_san(session.game, book_move.san)
            _show_board(session, flipped, hint=[offered.end] if offered else None)
            print(paint("   ┌─ THE SACRIFICE " + "─" * 40, YELLOW))
            print(f"   {paint(prefix + ' ' + book_move.san, BOLD, YELLOW)}"
                  f"   — offering {gambit.cost}, onto the marked square")
            _say(book_move.idea)
            print(paint("   └" + "─" * 56, YELLOW))
            session.push(book_move.san)
            _show_board(session, flipped)
            if pause and not _continue():
                return
            continue

        session.push(book_move.san)
        _show_board(session, flipped)
        print(f"   {paint(prefix + ' ' + book_move.san, BOLD)}")
        _say(book_move.idea)
        if book_move.mistakes:
            print(paint("\n   Instead:", DIM))
            _show_traps(book_move)
        if pause and ply < len(gambit.moves) - 1 and not _continue():
            return

    print(paint("\n   Final position: ", BOLD) + movelist(session.played))
    balance = _material_balance(session)
    print(f"   {paint('Material:', BOLD)} {balance}")
    print()
    _respond("Critical test:", gambit.test, YELLOW)
    _respond("Verdict:", gambit.verdict, CYAN)
    print(paint(f"\n   Drill it with:  drill {gambit.key}", DIM))


def _continue() -> bool:
    try:
        return input(paint("\n   [enter] next, 'q' to stop  ", DIM)).strip().lower() != "q"
    except EOFError:
        return False


def _soundness_colour(soundness: Soundness) -> str:
    return {
        Soundness.SOUND: GREEN,
        Soundness.SHARP: YELLOW,
        Soundness.POSITIONAL: CYAN,
        Soundness.DUBIOUS: RED,
        Soundness.NOT_A_GAMBIT: DIM,
    }[soundness]


# Standard piece values, used only to state the material count out loud.
_VALUES = {"Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, "K": 0}


def _material_balance(session: Session) -> str:
    """Who is up how much — the number the gambit is asking you to accept."""
    score = 0
    for row in session.game.board.squares:
        for piece in row:
            if piece is not None:
                value = _VALUES[piece.letter]
                score += value if piece.color is Color.WHITE else -value
    if score == 0:
        return "level"
    leader = "White" if score > 0 else "Black"
    return f"{leader} +{abs(score)} ({'pawn' if abs(score) == 1 else 'pawns'})"


def list_gambits() -> None:
    _heading("\nGambits")
    _say(
        "A gambit trades material for something else — time, lines, or "
        "pressure. The question is never 'is this a sacrifice' but 'is the "
        "compensation real'. These are ordered so you can compare."
    )
    for soundness in Soundness:
        group = gambits_mod.by_soundness(soundness)
        if not group:
            continue
        print(f"\n   {paint(soundness.value, _soundness_colour(soundness))}"
              f" {paint('— ' + soundness.blurb, DIM)}")
        for gambit in group:
            side = gambit.hero.value[0].upper()
            print(f"     {paint(gambit.key.ljust(13), BOLD)} {gambit.name}"
                  f"  {paint(f'[{gambit.eco}, {side}]', DIM)}")
    print(paint("\n   gambit <key>   show one    ·    gambit random   surprise me", DIM))


# --- explore ---------------------------------------------------------------
def explore() -> None:
    """Free play, with the coach naming the opening and flagging the exit."""
    _heading("\nExplore mode")
    _say(
        "Play any moves you like, for either side. I will tell you which "
        "openings are still in play and what the book recommends. 'book' lists "
        "the options, 'back' undoes a move, 'quit' exits."
    )

    session = Session()
    history: List[List[str]] = []

    while True:
        _show_board(session, flipped=False)
        candidates = book_mod.matching(session.played)
        if session.played:
            print("   " + movelist(session.played))
        if candidates:
            names = ", ".join(c.name for c in candidates[:3])
            more = f" (+{len(candidates) - 3} more)" if len(candidates) > 3 else ""
            _respond("In book:", f"{names}{more}", GREEN)
        elif session.played:
            print(f"   {paint('Out of book.', YELLOW)} No line in the repertoire plays this.")

        try:
            answer = input(paint("   move: ", BOLD)).strip()
        except EOFError:
            print()
            return
        if not answer:
            continue
        low = answer.lower()
        if low in ("quit", "q", "exit"):
            return
        if low == "back":
            if history:
                session = Session()
                for san in history.pop():
                    session.push(san)
            continue
        if low == "book":
            options = book_mod.next_moves(session.played)
            if not options:
                print("   Nothing in the book from here.")
            for line, bm in options:
                print(f"   {paint(bm.san, BOLD)} — {line.name}")
                _say(bm.idea)
            continue

        history.append(list(session.played))
        if not session.push(answer):
            history.pop()
            print(f"   {paint('Not a legal move.', RED)}")
            continue

        options = book_mod.next_moves(session.played[:-1])
        expected = [bm.san for _, bm in options]
        if expected and normalize(session.played[-1]) not in [normalize(e) for e in expected]:
            print(
                f"   {paint('That leaves the book.', YELLOW)} "
                f"The repertoire plays {', '.join(expected)} here."
            )


# --- menus -----------------------------------------------------------------
def list_lines() -> None:
    for side in (Color.WHITE, Color.BLACK):
        _heading(f"\nAs {side.value.title()}:")
        for line in book_mod.for_side(side):
            print(f"   {paint(line.key.ljust(12), BOLD)} {line.name}  {paint('[' + line.eco + ']', DIM)}")


def show_principles() -> None:
    _heading("\nOpening principles")
    _say(
        "Openings are memorised, but principles are what save you when your "
        "opponent leaves the book on move three — which they will."
    )
    for title, detail in PRINCIPLES:
        print(f"\n   {paint(title, BOLD)}")
        _say(detail)


HELP = """
Commands
   list                 the openings in the repertoire
   learn <key>          walk through a line with the reasoning
   drill <key>          play your side from memory; I correct you
   explore              free play, with the opening named as you go
   principles           the general rules that outlast any single line
   random               drill a line picked at random
   help                 this text
   quit                 leave
"""


def repl() -> None:
    _heading("Chess Opening Coach")
    _say(
        "An opening is not a sequence to memorise — it is a set of ideas about "
        "where the pieces belong and which pawn break matters. Type 'list' to "
        "see the repertoire, or 'help' for commands."
    )

    while True:
        try:
            raw = input(paint("\ncoach> ", BOLD, CYAN)).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]

        if command in ("quit", "q", "exit"):
            return
        if command in ("help", "?"):
            print(HELP)
        elif command == "list":
            list_lines()
        elif command == "principles":
            show_principles()
        elif command == "explore":
            explore()
        elif command == "random":
            drill(random.choice(book_mod.LINES))
        elif command in ("learn", "drill"):
            if not args:
                print(f"   Which opening? Try: {command} italian")
                continue
            line = book_mod.get(args[0])
            if line is None:
                print(f"   No opening called {args[0]!r}. Type 'list' to see them.")
                continue
            (learn if command == "learn" else drill)(line)
        else:
            print(f"   Unknown command {command!r}. Type 'help'.")


# --- self-check ------------------------------------------------------------
def selftest(verbose: bool = True) -> int:
    """Validate every line and every trap against the real engine.

    Returns the number of problems found. This is the check that matters: a
    coach that teaches an illegal move is worse than no coach.
    """
    from .san import replay

    problems = 0
    for line in book_mod.LINES:
        # 1. Every book move must be legal, and must round-trip through SAN
        #    exactly as written (catches "Nxd2" where "Nbxd2" is required).
        game = Game()
        for ply, book_move in enumerate(line.moves, start=1):
            move = from_san(game, book_move.san)
            if move is None:
                print(f"FAIL {line.key} ply {ply}: illegal move {book_move.san!r}")
                problems += 1
                break
            canonical = to_san(game, move)
            if canonical != book_move.san:
                print(f"FAIL {line.key} ply {ply}: wrote {book_move.san!r}, engine says {canonical!r}")
                problems += 1
            game.move(move)

            # 2. Every listed mistake must itself be a legal alternative at
            #    that exact point — otherwise the refutation is nonsense.
            for wrong, _why in book_move.mistakes:
                before = replay(line.sans[: ply - 1])
                if from_san(before, wrong) is None:
                    print(f"FAIL {line.key} ply {ply}: trap {wrong!r} is not legal here")
                    problems += 1

        # 3. Alternating colours: even plies are White, odd are Black.
        if len(line.moves) % 2 == 1 and line.hero is Color.BLACK:
            print(f"WARN {line.key}: ends on a White move but teaches Black")

    if verbose:
        total_plies = sum(len(l.moves) for l in book_mod.LINES)
        total_traps = sum(len(m.mistakes) for l in book_mod.LINES for m in l.moves)
        status = "ok" if problems == 0 else f"{problems} problem(s)"
        print(
            f"{len(book_mod.LINES)} lines, {total_plies} plies, "
            f"{total_traps} traps validated against the engine: {status}"
        )
    return problems
