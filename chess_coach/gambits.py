"""Gambits — openings that pay material for something else.

A gambit is not just another line, so it does not reuse the plain `Line`
presentation. The lesson in a gambit is a *trade*: here is what you hand over,
here is what you get, and here is how to tell whether it was worth it. So the
data model carries the sacrifice explicitly — which ply it happens on, what it
costs, what it buys, and what the best answer is.

The set below is chosen to span the range on purpose. Some gambits are sound
(Evans), some are sharp and double-edged (King's), one is positional and pays
off in the endgame rather than an attack (Benko), one is objectively bad
(Englund), and one is famously not a gambit at all (the Queen's). Seeing the
bad one next to the good ones is the point: "sacrifice for activity" is only a
plan when the activity is real.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

from chess.constants import Color

from .book import BookMove, Line

W, B = Color.WHITE, Color.BLACK


class Soundness(Enum):
    """How well the compensation actually holds up."""

    SOUND = "Sound"  # objectively fine; played at the top level
    SHARP = "Sharp"  # playable, but one slip either way decides it
    POSITIONAL = "Positional"  # compensation is long-term, not an attack
    DUBIOUS = "Dubious"  # a trap opening; refuted by accurate play
    NOT_A_GAMBIT = "Not really a gambit"  # the material comes straight back

    @property
    def blurb(self) -> str:
        return {
            Soundness.SOUND: "played at the highest level; the compensation is real",
            Soundness.SHARP: "objectively balanced, but whoever knows it better wins",
            Soundness.POSITIONAL: "no attack — the payment is pressure that lasts into the endgame",
            Soundness.DUBIOUS: "works on the unprepared and loses to anyone who knows it",
            Soundness.NOT_A_GAMBIT: "the material is recovered by force; the offer is a deflection",
        }[self]


@dataclass(frozen=True)
class Gambit:
    key: str
    name: str
    eco: str
    hero: Color  # the side making the sacrifice
    soundness: Soundness
    cost: str  # what is handed over, in plain words
    compensation: Tuple[str, ...]  # what is bought
    sacrifice_ply: int  # 0-based index into `moves` of the offering move
    moves: Tuple[BookMove, ...]  # the main accepted line
    test: str  # the best answer / critical test
    verdict: str  # should you play it, and against whom

    @property
    def sans(self) -> List[str]:
        return [m.san for m in self.moves]

    @property
    def sacrifice(self) -> BookMove:
        return self.moves[self.sacrifice_ply]

    @property
    def line(self) -> Line:
        """A plain `Line` view, so gambits also work with learn/drill."""
        return Line(
            key=self.key,
            name=self.name,
            eco=self.eco,
            hero=self.hero,
            summary=f"{self.soundness.value}: {self.soundness.blurb}. "
            f"You give {self.cost} for {self.compensation[0][0].lower()}{self.compensation[0][1:]}",
            moves=self.moves,
            plans=self.compensation + (f"Critical test: {self.test}", f"Verdict: {self.verdict}"),
        )


GAMBITS: Tuple[Gambit, ...] = (
    Gambit(
        key="evans",
        name="Evans Gambit",
        eco="C51",
        hero=W,
        soundness=Soundness.SOUND,
        cost="one pawn",
        compensation=(
            "A tempo: the bishop on c5 is hit and must move again.",
            "c3 and d4 next, building the full centre with gain of time — the pawn buys the tempo that makes the centre free.",
            "An open b-file and fast queenside development.",
        ),
        sacrifice_ply=6,  # 4.b4
        moves=(
            BookMove("e4", "The classical start."),
            BookMove("e5", "Symmetry."),
            BookMove("Nf3", "Attacking e5."),
            BookMove("Nc6", "Defending it."),
            BookMove("Bc4", "The Italian bishop, aimed at f7."),
            BookMove("Bc5", "The Giuoco Piano — and the position the gambit is built to exploit."),
            BookMove("b4", "The gambit. The pawn is *en prise* to the bishop and cannot be defended — that is the point. Every move Black spends taking and retreating is a move White spends building."),
            BookMove("Bxb4", "Accepting. Declining with 4...Bb6 is respectable and leaves White a useful tempo anyway."),
            BookMove("c3", "Hitting the bishop again. Two tempi bought for one pawn."),
            BookMove("Ba5", "The main retreat, keeping the bishop on the a5-e1 diagonal to annoy c3.",
                     (("Be7", "Solid and modern — the bishop steps out of the way rather than inviting more tempo gains."),)),
            BookMove("d4", "The payoff. White has the ideal centre, a lead in development, and open lines, for the price of one pawn."),
        ),
        test="4...Bxb4 5.c3 Be7! — the modern retreat, sidestepping the tempo-gaining attacks on the bishop.",
        verdict="Genuinely good. Morphy played it, Kasparov revived it against Anand in 1995. The soundest attacking gambit in chess.",
    ),
    Gambit(
        key="kingsgambit",
        name="King's Gambit Accepted, Kieseritzky",
        eco="C39",
        hero=W,
        soundness=Soundness.SHARP,
        cost="one pawn, and the safety of your own king",
        compensation=(
            "A pawn majority in the centre: d4 and e4 roll forward unopposed.",
            "The half-open f-file, pointing straight at f7.",
            "A huge initiative — Black must find accurate moves immediately.",
        ),
        sacrifice_ply=2,  # 2.f4
        moves=(
            BookMove("e4", "The classical start."),
            BookMove("e5", "Symmetry."),
            BookMove("f4", "The King's Gambit — the great romantic opening of the 19th century. It offers a pawn to deflect Black's e5 pawn and claim the whole centre. The cost is real: the f-pawn was shielding White's king."),
            BookMove("exf4", "Accepting. Declining with 2...Bc5 is a serious option that stops White castling comfortably."),
            BookMove("Nf3", "Developing, and pre-empting the check on h4 that would otherwise come with tempo."),
            BookMove("g5", "Black clings to the extra pawn and builds a chain. Greedy, principled, and exactly what White is hoping for — those kingside pawns will become weak."),
            BookMove("h4", "Undermining the chain at once, before Black consolidates."),
            BookMove("g4", "Pushing past and attacking the knight."),
            BookMove("Ne5", "The Kieseritzky. The knight steps into the centre rather than retreating, eyeing f7 and g4, and the game becomes a calculation contest."),
        ),
        test="3...d5! — the Modern Defence. Instead of grabbing with ...g5, Black returns the pawn immediately to open lines and develop. This is why the King's Gambit is not seen at the top level.",
        verdict="Enormous fun and completely playable below master level. Above it, the ...d5 lines mean you are working hard for equality.",
    ),
    Gambit(
        key="danish",
        name="Danish Gambit",
        eco="C21",
        hero=W,
        soundness=Soundness.SHARP,
        cost="two pawns",
        compensation=(
            "Two bishops raking the long diagonals at f7 and g7 — the most beautiful piece placement in the opening.",
            "A lead in development of three or four tempi.",
            "Black's king has no safe square while the bishops are aimed at it.",
        ),
        sacrifice_ply=4,  # 3.c3
        moves=(
            BookMove("e4", "The classical start."),
            BookMove("e5", "Symmetry."),
            BookMove("d4", "The Centre Game — striking at once."),
            BookMove("exd4", "Effectively forced."),
            BookMove("c3", "The Danish. White offers a second pawn to open the c-file and clear the b2 square for the dark-squared bishop."),
            BookMove("dxc3", "Accepting. Black can also decline with 3...d5!, returning material for free development."),
            BookMove("Bc4", "The first bishop takes aim at f7 — before recapturing, because development is the whole point."),
            BookMove("cxb2", "Taking the second pawn. Black is two pawns up and four tempi down."),
            BookMove("Bxb2", "Both bishops are now on the great diagonals. White has no material and a winning-looking position — which is exactly the illusion to be careful of."),
        ),
        test="5...d5! — Black gives both pawns straight back to blunt the bishops and finish developing. After 6.Bxd5 Nf6 the position is level.",
        verdict="Spectacular against an unprepared opponent, harmless against a prepared one. Learn it to understand development; do not build a career on it.",
    ),
    Gambit(
        key="smithmorra",
        name="Smith-Morra Gambit",
        eco="B21",
        hero=W,
        soundness=Soundness.SHARP,
        cost="one pawn",
        compensation=(
            "Two open files — c and d — pointing at Black's queenside and centre.",
            "Rapid development: Nc3, Bc4, Nf3, O-O, Rc1, Qe2 all come with purpose.",
            "It denies the Sicilian player their own game — no Najdorf, no Dragon, no thirty moves of preparation.",
        ),
        sacrifice_ply=4,  # 3.c3
        moves=(
            BookMove("e4", "White's first move."),
            BookMove("c5", "The Sicilian — the most common answer to 1.e4, and the reason this gambit exists."),
            BookMove("d4", "Immediately challenging, rather than entering the Open Sicilian with 2.Nf3."),
            BookMove("cxd4", "Black takes, as in every Sicilian."),
            BookMove("c3", "The Smith-Morra. White offers the c-pawn to open the c-file and skip the entire Open Sicilian."),
            BookMove("dxc3", "Accepting. Declining with 3...Nf6 or 3...d3 is common and respectable — many strong players simply refuse."),
            BookMove("Nxc3", "The knight develops to its best square *and* recaptures. White is a pawn down with a big lead in development and two open files."),
        ),
        test="3...Nf6! or 3...d3 — declining. Against a prepared Sicilian player who declines, White has an ordinary position, not an attack.",
        verdict="The most practical answer to the Sicilian for a club player. It trades a pawn for not needing to learn the Open Sicilian, which is a very good trade if your study time is limited.",
    ),
    Gambit(
        key="marshall",
        name="Marshall Attack",
        eco="C89",
        hero=B,
        soundness=Soundness.SOUND,
        cost="one pawn",
        compensation=(
            "A raging kingside attack: the queen swings to h4, the bishops point at h2 and the rook lifts to e6.",
            "White's pieces are all on the queenside and cannot come back in time.",
            "Every piece Black has left plays; White defends with the king alone.",
        ),
        sacrifice_ply=15,  # 8...d5
        moves=(
            BookMove("e4", "The classical start."),
            BookMove("e5", "Symmetry."),
            BookMove("Nf3", "Attacking e5."),
            BookMove("Nc6", "Defending."),
            BookMove("Bb5", "The Ruy Lopez."),
            BookMove("a6", "The Morphy Defence."),
            BookMove("Ba4", "Keeping the diagonal."),
            BookMove("Nf6", "Hitting e4."),
            BookMove("O-O", "White ignores the pawn — king safety first."),
            BookMove("Be7", "Preparing to castle."),
            BookMove("Re1", "Defending e4 properly."),
            BookMove("b5", "Kicking the bishop."),
            BookMove("Bb3", "The bishop's permanent home."),
            BookMove("O-O", "Black castles, and White expects the quiet 8...d6."),
            BookMove("c3", "Preparing d4 — the normal Spanish plan."),
            BookMove("d5", "The Marshall! Instead of the solid ...d6, Black throws in the centre and gives up e5. Frank Marshall reputedly saved this for eight years before playing it against Capablanca in 1918."),
            BookMove("exd5", "Accepting. Declining with 9.d4 is the modern 'Anti-Marshall' preference precisely because the attack is so dangerous."),
            BookMove("Nxd5", "Recapturing with the knight, heading for f4 or b6."),
            BookMove("Nxe5", "White wins the pawn."),
            BookMove("Nxe5", "Trading off the defender."),
            BookMove("Rxe5", "White is a clean pawn up. And now the point:"),
            BookMove("c6", "A quiet little move that props up d5 and opens the b7-h1 diagonal for the bishop. Black has no threats yet — and a permanent initiative. This is compensation you have to trust rather than calculate."),
        ),
        test="The Anti-Marshall: 8.a4 or 8.h3 instead of 8.c3, sidestepping the whole thing. Most strong players simply avoid it.",
        verdict="Completely sound and still played at the top level after a century. The purest example of a positional pawn sacrifice for an attack.",
    ),
    Gambit(
        key="benko",
        name="Benko (Volga) Gambit",
        eco="A57",
        hero=B,
        soundness=Soundness.POSITIONAL,
        cost="one pawn",
        compensation=(
            "Two open files, a and b, aimed at White's queenside — permanently.",
            "The g7 bishop rakes the long diagonal for the entire game.",
            "Uniquely among gambits, the compensation *survives into the endgame*. Trading queens does not help White.",
        ),
        sacrifice_ply=5,  # 3...b5
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("Nf6", "The hypermodern reply."),
            BookMove("c4", "Grabbing space."),
            BookMove("c5", "Striking at d4 immediately."),
            BookMove("d5", "White pushes past, gaining space."),
            BookMove("b5", "The Benko. Black offers a wing pawn to blow open the queenside — not for an attack on the king, but for pressure that never goes away."),
            BookMove("cxb5", "Accepting."),
            BookMove("a6", "The follow-up, and the real gambit move: Black insists on opening the a-file too."),
            BookMove("bxa6", "Taking the second offer. White can also decline with 5.b6 or 5.e3."),
            BookMove("Bxa6", "Black has one pawn for nothing and two open files. The bishop hits White's queenside from a6, and ...g6, ...Bg7, ...O-O, ...Ra7 and ...Qa8 all follow naturally."),
        ),
        test="The Fianchetto lines with 5.b6 or an early e3, giving the pawn back to blunt the pressure before it becomes chronic.",
        verdict="The best example in chess of a *strategic* sacrifice. If you only ever learn one gambit for the understanding rather than the tricks, learn this one.",
    ),
    Gambit(
        key="budapest",
        name="Budapest Gambit",
        eco="A51",
        hero=B,
        soundness=Soundness.SHARP,
        cost="one pawn, temporarily",
        compensation=(
            "Immediate piece activity — the knight lands on g4 or e4 and makes threats from move three.",
            "Black usually regains the pawn by force, so the real gain is time and surprise.",
            "It takes a 1.d4 player straight out of their preparation.",
        ),
        sacrifice_ply=3,  # 2...e5
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("Nf6", "The standard reply."),
            BookMove("c4", "Building the big centre."),
            BookMove("e5", "The Budapest. Black throws a pawn at the centre on move two — a genuine shock if White has not seen it."),
            BookMove("dxe5", "Accepting. Declining with 3.d5 or 3.Nf3 is entirely playable."),
            BookMove("Ng4", "The point. The knight attacks e5 and heads for the juicy squares on e5 and c5. Black will usually win the pawn straight back.",
                     (("Ne4", "The Fajarowicz Variation — sharper, rarer, and objectively worse. A specialist's weapon."),)),
        ),
        test="4.Bf4 or 4.Nf3 — calm development, holding the pawn for a while and giving it back on White's terms.",
        verdict="A fine surprise weapon at club level. Not a main-line defence, but a real opening rather than a trap.",
    ),
    Gambit(
        key="englund",
        name="Englund Gambit",
        eco="A40",
        hero=B,
        soundness=Soundness.DUBIOUS,
        cost="one pawn, with no real compensation",
        compensation=(
            "One idea only: the trap 4...Qb4+ hitting b2 and the bishop, hoping for 5.Bd2?? Qxb2 with a fork.",
            "Surprise value against someone who has never met it.",
            "That is the whole list — which is exactly the lesson.",
        ),
        sacrifice_ply=1,  # 1...e5
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("e5", "The Englund Gambit. Black offers a pawn with no development, no centre, and no open lines to show for it. Included here as the counterexample: this is what insufficient compensation looks like."),
            BookMove("dxe5", "Accepting, correctly. White is simply a pawn up."),
            BookMove("Nc6", "Developing with a hit on the pawn."),
            BookMove("Nf3", "Defending it and developing."),
            BookMove("Qe7", "The trap is loaded: Black threatens ...Qb4+ picking up b2."),
            BookMove("Bf4", "Natural and good — but it walks toward the trick."),
            BookMove("Qb4+", "The point. Black checks and attacks b2 at the same time. If White plays 5.Bd2?? then 5...Qxb2 hits the rook and the bishop at once."),
        ),
        test="5.Bd2 Qxb2 6.Bc3! — the refutation. The bishop steps onto c3 to trap the queen, and after 6...Bb4 7.Qd2 White is winning.",
        verdict="Do not play this. It is here so you can recognise the trap when someone plays it at you, and so you can see the difference between a gambit and a hope.",
    ),
    Gambit(
        key="queensgambit",
        name="The Queen's Gambit (which is not one)",
        eco="D06",
        hero=W,
        soundness=Soundness.NOT_A_GAMBIT,
        cost="nothing, in the end",
        compensation=(
            "The c-pawn cannot be held: after 2...dxc4 3.e3, any attempt to defend it loses material.",
            "The real purpose is deflection — trading a wing pawn for Black's centre pawn, so White's e-pawn can advance.",
            "White regains the pawn whenever they choose, usually with Bxc4.",
        ),
        sacrifice_ply=2,  # 2.c4
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("d5", "Black matches."),
            BookMove("c4", "The Queen's Gambit — the most famous 'gambit' in chess, and a misnomer. The pawn is offered, but it is never really given."),
            BookMove("dxc4", "Accepting."),
            BookMove("e3", "Preparing Bxc4. White makes no attempt to rush; the pawn is not going anywhere."),
            BookMove("Nf6", "Correct: Black develops and does *not* try to hold the extra pawn.",
                     (("b5", "The refutation of greed: 4.a4! c6 5.axb5 cxb5 6.Qf3! forks the a8 rook and the b5 pawn. Black loses material trying to keep a pawn that was never theirs."),)),
            BookMove("Bxc4", "And the pawn comes back. Material is level, and White has traded a c-pawn for a d-pawn — a small, permanent central gain."),
        ),
        test="There is no test. The pawn returns by force in every line.",
        verdict="Included to sharpen the definition. A gambit means material for something else; here the material comes back. Knowing the difference tells you when you actually have to attack.",
    ),
)


BY_KEY: Dict[str, Gambit] = {g.key: g for g in GAMBITS}


def get(key: str) -> Optional[Gambit]:
    return BY_KEY.get(key.strip().lower())


def for_side(hero: Color) -> List[Gambit]:
    return [g for g in GAMBITS if g.hero is hero]


def by_soundness(soundness: Soundness) -> List[Gambit]:
    return [g for g in GAMBITS if g.soundness is soundness]
