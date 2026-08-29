"""Entry point.

    python -m chess_coach                 interactive coach
    python -m chess_coach --selftest      validate the book, print nothing else
    python -m chess_coach --drill italian jump straight into a drill
    python -m chess_coach --learn ruylopez --no-pause    print a whole line
"""

from __future__ import annotations

import argparse
import sys

from . import book as book_mod
from . import gambits as gambits_mod
from .coach import (
    drill,
    explore,
    learn,
    list_gambits,
    list_lines,
    repl,
    resolve,
    selftest,
    show_gambit,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chess_coach", description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="validate every book line against the engine")
    parser.add_argument("--list", action="store_true", help="list the openings and exit")
    parser.add_argument("--learn", metavar="KEY", help="walk through one opening")
    parser.add_argument("--drill", metavar="KEY", help="drill one opening")
    parser.add_argument("--explore", action="store_true", help="free play with opening identification")
    parser.add_argument("--no-pause", action="store_true", help="with --learn, do not wait for enter")
    args = parser.parse_args(argv)

    if args.selftest:
        return 1 if selftest() else 0
    if args.list:
        list_lines()
        return 0
    if args.explore:
        explore()
        return 0

    key = args.learn or args.drill
    if key:
        line = book_mod.get(key)
        if line is None:
            print(f"No opening called {key!r}. Known: {', '.join(book_mod.BY_KEY)}", file=sys.stderr)
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
