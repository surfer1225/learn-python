"""Entry point.

    python -m chess_coach                 interactive coach
    python -m chess_coach --selftest      validate the book, print nothing else
    python -m chess_coach --drill italian jump straight into a drill
    python -m chess_coach --gambits       list the gambits by soundness
    python -m chess_coach --gambit evans  show one gambit's trade
    python -m chess_coach --learn ruylopez --no-pause    print a whole line
    python -m chess_coach --spar black --level strong    play a game against the AI
    python -m chess_coach --ask "how do I meet 1.d4?"    one question, one answer
"""

from __future__ import annotations

import argparse
import sys

from chess.constants import Color

from . import book as book_mod
from . import gambits as gambits_mod
from .coach import (
    ai_status,
    ask,
    drill,
    explore,
    learn,
    list_gambits,
    list_lines,
    repl,
    resolve,
    selftest,
    set_ai,
    show_gambit,
    spar,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chess_coach", description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="validate every book line against the engine")
    parser.add_argument("--list", action="store_true", help="list the openings and exit")
    parser.add_argument("--learn", metavar="KEY", help="walk through one opening")
    parser.add_argument("--drill", metavar="KEY", help="drill one opening")
    parser.add_argument("--explore", action="store_true", help="free play with opening identification")
    parser.add_argument("--gambit", metavar="KEY", help="show a gambit: what it costs and what it buys")
    parser.add_argument("--gambits", action="store_true", help="list the gambits by soundness and exit")
    parser.add_argument("--no-pause", action="store_true", help="with --learn/--gambit, do not wait for enter")

    ai = parser.add_argument_group("the AI coach")
    ai.add_argument("--spar", nargs="?", const="white", choices=("white", "black"),
                    metavar="SIDE", help="play a whole game against the AI coach")
    ai.add_argument("--level", default="club", choices=("beginner", "club", "strong"),
                    help="how hard the AI coach plays when sparring (default: club)")
    ai.add_argument("--ask", metavar="QUESTION", help="ask one question about the starting position and exit")
    ai.add_argument("--no-ai", action="store_true", help="never call the model, whatever is configured")
    ai.add_argument("--ai-status", action="store_true", help="report whether the model is reachable and exit")
    args = parser.parse_args(argv)

    # Muting has to happen before any mode starts, since the modes announce
    # the coach's state on the way in.
    if args.no_ai:
        set_ai(False, announce=False)

    if args.ai_status:
        print(f"AI coach: {ai_status()}")
        return 0
    if args.selftest:
        return 1 if selftest() else 0
    if args.list:
        list_lines()
        return 0
    if args.gambits:
        list_gambits()
        return 0
    if args.ask:
        _ask_about(Session(), args.ask)
        return 0
    if args.spar:
        spar(Color.BLACK if args.spar == "black" else Color.WHITE, level=args.level)
        return 0
    if args.explore:
        explore()
        return 0

    if args.gambit:
        gambit = gambits_mod.get(args.gambit)
        if gambit is None:
            print(
                f"No gambit called {args.gambit!r}. Known: {', '.join(gambits_mod.BY_KEY)}",
                file=sys.stderr,
            )
            return 2
        show_gambit(gambit, pause=not args.no_pause)
        return 0

    key = args.learn or args.drill
    if key:
        line = resolve(key)
        if line is None:
            known = list(book_mod.BY_KEY) + list(gambits_mod.BY_KEY)
            print(f"No opening called {key!r}. Known: {', '.join(known)}", file=sys.stderr)
            return 2
        if args.learn:
            learn(line, pause=not args.no_pause)
        else:
            drill(line)
        return 0

    repl()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
