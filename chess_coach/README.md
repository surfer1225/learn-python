# Chess Opening Coach

A terminal coach that teaches openings by making you play them, not read them.

```
python -m chess_coach                     # interactive
python -m chess_coach --list              # what's in the repertoire
python -m chess_coach --gambits           # the gambits, by soundness
python -m chess_coach --gambit evans      # show one gambit's trade
python -m chess_coach --drill italian     # straight into a drill
python -m chess_coach --learn kid --no-pause
python -m chess_coach --selftest          # validate the book against the engine

python -m chess_coach --spar black        # a whole game against the AI coach
python -m chess_coach --ask "how do I meet 1.d4?"
python -m chess_coach --ai-status         # is the model reachable, and which one
```

## Two coaches

There are two coaches in here and the split between them is the whole design.

The **book coach** is data plus the engine. It is always right, always instant,
always free, and it knows exactly thirteen openings. The **AI coach** is a
language model. It knows every position there is, and it is the only one of the
two that can be wrong.

So they are asked different questions. Where they overlap, the book wins: a
trap it has a refutation for gets the book's refutation, because that was
written by someone who knew and it is the same every time. The model is asked
only what the book cannot answer — why *your* move was worse, what the plan
behind the one sentence actually is, and what to do in the several million
positions nobody wrote down.

The AI coach is optional. Without credentials the other four modes are
untouched and the trainer says one line about what to set.

## The five modes

| Mode | What it does | When to use it |
| --- | --- | --- |
| `learn <key>` | Walks the line move by move with the reasoning and the traps | First encounter with an opening |
| `drill <key>` | You play your side from memory; the coach replies and corrects | Every session after the first |
| `gambit <key>` | Shows a sacrifice: what it costs, what it buys, and whether that's a fair price | Understanding *why* a sacrifice works |
| `explore` | Free play; the coach names which openings are still live and flags the move that leaves the book | Reviewing one of your own games |
| `spar` | A whole game against the AI coach, with a word on every move you play | After the book runs out, around move ten |

`drill` is the one that works. Reading a line teaches you to *recognise* it;
being asked for the move with nothing on screen but the board teaches you to
*find* it. The coach grades three kinds of wrong differently:

- **A known trap** gets its refutation ("4.Qxf7# is mate").
- **A legal but inferior move** gets the book move — and, if the AI coach is
  connected, what the move cost you. This is the gap the book cannot close: it
  carries a refutation for every trap it knows about, but a learner's inferior
  move is usually not a trap, it is a sensible move that quietly concedes
  something, and there is no way to enumerate those in advance.
- **A typo or illegal move** gets a nudge and doesn't count against you.

Real output, from `drill italian` after answering `Nc3` on move three:

> Nc3 isn't a mistake — it's the Four Knights, fully sound, and you lose
> nothing by force. What it costs you is your *plan*. The whole Giuoco Piano is
> built on c3 and d4, hitting the centre with a pawn while the bishop on c4
> already eyes f7. Put the knight on c3 and that c-pawn is locked in behind it
> forever.
>
> `Move: Bc4`  ·  `Line: 3. Bc4 Bc5  4. c3 Nf6  5. d4 exd4  6. cxd4 Bb4+`

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

## Gambits

Nine gambits, deliberately spanning the quality range rather than just listing
famous ones. Each shows the trade explicitly — the board pauses at the moment
of sacrifice with the square marked — and ends with the critical test and a
verdict.

| Soundness | Gambits |
| --- | --- |
| **Sound** — real compensation, played at the top | `evans`, `marshall` |
| **Sharp** — balanced, but whoever knows it better wins | `kingsgambit`, `danish`, `smithmorra`, `budapest` |
| **Positional** — pressure that survives into the endgame | `benko` |
| **Dubious** — a trap; refuted by accurate play | `englund` |
| **Not really a gambit** — the material comes straight back | `queensgambit` |

The last two rows carry the lesson. The Englund shows what *insufficient*
compensation looks like, and the Queen's Gambit is in the set because it is
famously misnamed — the pawn cannot be held, so nothing is actually given. Put
next to the Evans, they sharpen the definition: a gambit is material for
something else, and you have to be able to name the something else.

Gambit keys work with `learn` and `drill` too — `drill evans` treats it as an
ordinary line.

## How it's built

```
book.py      the repertoire: pure data, one sentence of "why" per move
gambits.py   the gambits: sacrifice ply, cost, compensation, verdict
san.py       Standard Algebraic Notation <-> the engine's Move objects
render.py    terminal board drawing
coach.py     the four modes, the REPL, and the self-check
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

**The book validates itself.** `--selftest` replays every line through the real
engine and checks that each move is legal, that each SAN string is *exactly*
what the engine renders, and that each listed trap is a legal alternative at
that point. A typo in the book is a test failure, not a coach confidently
teaching an illegal move.

Gambits get an extra check the openings don't need: the sacrifice must belong
to the side making it, and **the gambiteer must actually end up down material**,
counted off the real board rather than taken from the prose. This caught a bug
in the check itself — the Smith-Morra measures as level across the sacrifice
because White is already a pawn down pending recapture when 3.c3 is played, so
the invariant had to be "down relative to an even start", not "down relative to
the move before".

```
$ python -m chess_coach --selftest
13 lines + 9 gambits, 220 plies, 31 traps validated against the engine: ok
```

## Tests

```
PYTHONPATH=. python tests/test_chess_coach.py
python -m pytest tests/test_chess_coach.py
```
