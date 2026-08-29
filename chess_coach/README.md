# Chess Opening Coach

A terminal coach that teaches openings by making you play them, not read them.

```
python -m chess_coach                     # interactive
python -m chess_coach --list              # what's in the repertoire
python -m chess_coach --drill italian     # straight into a drill
python -m chess_coach --learn kid --no-pause
python -m chess_coach --selftest          # validate the book against the engine
```

## The three modes

| Mode | What it does | When to use it |
| --- | --- | --- |
| `learn <key>` | Walks the line move by move with the reasoning and the traps | First encounter with an opening |
| `drill <key>` | You play your side from memory; the coach replies and corrects | Every session after the first |
| `explore` | Free play; the coach names which openings are still live and flags the move that leaves the book | Reviewing one of your own games |

`drill` is the one that works. Reading a line teaches you to *recognise* it;
being asked for the move with nothing on screen but the board teaches you to
*find* it. The coach grades three kinds of wrong differently:

- **A known trap** gets its refutation ("4.Qxf7# is mate").
- **A legal but inferior move** gets the book move and moves on.
- **A typo or illegal move** gets a nudge and doesn't count against you.

## The repertoire

Thirteen lines, chosen so that one coherent repertoire exists for each colour
rather than thirty disconnected fragments.

| Key | Opening | Side |
| --- | --- | --- |
| `italian` | Italian Game, Giuoco Piano | White |
| `ruylopez` | Ruy Lopez, Closed (Morphy Defence) | White |
| `scotch` | Scotch Game | White |
| `friedliver` | Two Knights: Fried Liver Attack | White |
| `london` | London System | White |
| `sicilian` | Sicilian Defence, Najdorf | Black |
| `french` | French Defence, Winawer | Black |
| `carokann` | Caro-Kann, Classical | Black |
| `qgd` | Queen's Gambit Declined | Black |
| `qga` | Queen's Gambit Accepted | Black |
| `slav` | Slav Defence | Black |
| `kid` | King's Indian Defence | Black |
| `scholars` | Refuting Scholar's Mate | Black |

Plus `principles` — the general rules that keep you alive when your opponent
leaves the book on move three, which they will.

## How it's built

```
book.py      the repertoire: pure data, one sentence of "why" per move
san.py       Standard Algebraic Notation <-> the engine's Move objects
render.py    terminal board drawing
coach.py     the three modes, the REPL, and the self-check
```

**The engine is reused from `chess/`, not reimplemented.** Legality, check,
castling, en passant and promotion are already correct there. A coach with its
own move generator would eventually disagree with the game about what is legal,
and the coach would be the one that's wrong.

**SAN parsing has no grammar.** `to_san` renders a move; `from_san` generates
every legal move, renders each, and matches the string. That is O(legal moves)
per parse — about 5 ms — and it buys a guarantee: the two directions cannot
disagree, so disambiguation (`Nbxd2`), check suffixes (`Bb4+`), and castling
come out consistent for free. The property this relies on is that SAN is
injective over a position's legal moves, which the tests assert directly over
240 random positions.

**The book validates itself.** `--selftest` replays all 13 lines through the
real engine and checks that every move is legal, that every SAN string is
*exactly* what the engine renders, and that every listed trap is a legal
alternative at that point. A typo in the book is a test failure, not a coach
confidently teaching an illegal move.

```
$ python -m chess_coach --selftest
13 lines, 131 plies, 28 traps validated against the engine: ok
```

## Tests

```
PYTHONPATH=. python tests/test_chess_coach.py
python -m pytest tests/test_chess_coach.py
```
