"""The opening repertoire the coach teaches from.

Design note: this file is *data*, not logic. Every line is a sequence of SAN
moves, each carrying the one sentence that explains why the move is played.
`chess_coach.san.replay` validates every line against the real engine at
import-time in the self-test, so a typo here becomes a test failure rather than
a coach confidently teaching an illegal move.

Commentary rule followed throughout: say what the move *achieves*, never what
it *does*. "Nf3" does not need "develops the knight to f3" — the learner can
see that. It needs "attacks e5, so Black must react instead of building their
own plan."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from chess.constants import Color


@dataclass(frozen=True)
class BookMove:
    """One ply, with the idea behind it and the traps around it."""

    san: str
    idea: str
    # (wrong move, why it fails) — surfaced when the learner plays it, and as
    # "traps to know" during a walkthrough.
    mistakes: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Line:
    key: str  # short slug used on the command line
    name: str
    eco: str  # ECO classification code, so the learner can look it up
    hero: Color  # the side whose repertoire this is
    summary: str
    moves: Tuple[BookMove, ...]
    plans: Tuple[str, ...] = ()

    @property
    def sans(self) -> List[str]:
        return [m.san for m in self.moves]

    def __str__(self) -> str:
        return f"{self.name} ({self.eco})"


W, B = Color.WHITE, Color.BLACK


# --- Shared opening principles, shown by `principles` ----------------------
PRINCIPLES: Tuple[Tuple[str, str], ...] = (
    (
        "Fight for the centre",
        "The four central squares are where pieces reach the most ground. A "
        "knight on e5 touches eight squares; on a1 it touches two.",
    ),
    (
        "Develop toward the centre, knights before bishops",
        "Knights have only one good square each early on, so they are easy to "
        "commit. Bishops want to see how the pawns settle before choosing a "
        "diagonal.",
    ),
    (
        "Castle early",
        "The king is a liability until move 40 and an asset after. Get it off "
        "the open central files before the position opens.",
    ),
    (
        "Do not move the same piece twice in the opening",
        "Every repeat move is a move your opponent spends on a new piece. "
        "Exception: when the repeat wins material or forces a concession.",
    ),
    (
        "Do not bring the queen out early",
        "She is the one piece every enemy developing move can attack. Each "
        "time she is chased, your opponent develops for free.",
    ),
    (
        "f7 and f2 are the weak squares",
        "At the start they are defended by the king alone. Nearly every early "
        "trap in chess aims there.",
    ),
)


LINES: Tuple[Line, ...] = (
    # ---------------------------------------------------------------- e4 e5
    Line(
        key="italian",
        name="Italian Game, Giuoco Piano",
        eco="C53",
        hero=W,
        summary=(
            "The most natural opening in chess: every piece goes to its best "
            "square and White builds a big pawn centre with c3 and d4. The "
            "right first opening for almost anyone playing 1.e4."
        ),
        moves=(
            BookMove("e4", "Takes the centre and frees two pieces — the queen and the light-squared bishop — with one pawn move."),
            BookMove("e5", "Black stakes an equal claim. Symmetry is fine here; the player who develops with more purpose gets the better game."),
            BookMove("Nf3", "Develops *with a threat*. Attacking e5 means Black must answer instead of pursuing their own plan.",
                     (("Qh5", "The queen sortie. After 2...Nc6 3.Bc4 g6 she is chased around the board and Black develops with tempo every time."),
                      ("f4", "The King's Gambit — playable and sharp, but it hands Black open lines at your own king. Not a first repertoire."))),
            BookMove("Nc6", "Defends e5 and develops. The only move that does both.",
                     (("f6", "Damiano's Defence, and a genuine blunder: 3.Nxe5! fxe5 4.Qh5+ leaves Black's king naked and losing."),
                      ("d6", "Philidor's Defence. Solid but passive — it blocks the f8 bishop and cedes the centre without a fight."))),
            BookMove("Bc4", "The bishop's best diagonal: it stares at f7, the one square defended by nothing but Black's king."),
            BookMove("Bc5", "Black mirrors, eyeing f2. This is the Giuoco Piano, 'the quiet game'.",
                     (("Nf6", "Perfectly good — the Two Knights Defence — but it invites 4.Ng5 and a much sharper game. See the 'friedliver' line."),)),
            BookMove("c3", "Quiet but purposeful: it prepares d4 to build the big centre. The price is that the b1 knight loses its natural square.",
                     (("Nxe5", "Simply drops a piece: the knight on c6 defends e5, so 4...Nxe5 wins a piece for a pawn."),
                      ("O-O", "Safe and fine, but c3 first is more testing — it fights for d4 before Black can consolidate."))),
            BookMove("Nf6", "Develops and hits e4, so Black gets a say in the centre rather than waiting."),
            BookMove("d4", "The point of c3. White claims the full centre while Black's pieces are not yet coordinated."),
            BookMove("exd4", "Black must take — leaving the tension lets White play dxe5 with a clear space edge."),
            BookMove("cxd4", "Recapturing toward the centre. White now has pawns on d4 and e4, the ideal duo."),
            BookMove("Bb4+", "A useful check: it develops, and forces White to spend a move resolving it before consolidating."),
            BookMove("Bd2", "The calm answer. Blocking with the bishop offers a trade that takes the sting out of Black's initiative.",
                     (("Nc3", "The Greco Attack — a real gambit line, but it invites 7...Nxe4 and a forcing sequence you need to know by heart."),
                      ("Kf1", "Never do this without a concrete reason. It loses castling rights and buries the h1 rook."))),
            BookMove("Bxd2+", "Trading off the piece that was doing the annoying work."),
            BookMove("Nbxd2", "Note the disambiguation: *either* knight could take on d2. The b1 knight goes, keeping f3 guarding the centre."),
            BookMove("d5", "Black's freeing break. Without it, White's centre simply rolls forward."),
            BookMove("exd5", "Opening the position while White is the better developed side — exactly when you want lines to open."),
            BookMove("Nxd5", "Black recaptures with the knight, reaching an even but lively middlegame."),
        ),
        plans=(
            "White: castle, put a rook on e1, and use the extra central space to build a kingside attack.",
            "White: the isolated d-pawn is a strength while pieces remain — it grants e5 and c5 as outposts.",
            "Black: blockade d5 with a knight and trade pieces; the isolated pawn becomes a weakness in the endgame.",
        ),
    ),
    Line(
        key="ruylopez",
        name="Ruy Lopez, Closed (Morphy Defence)",
        eco="C84",
        hero=W,
        summary=(
            "The most respected opening in chess, played at world championship "
            "level for 150 years. White applies slow pressure to e5 and spends "
            "the opening manoeuvring rather than attacking."
        ),
        moves=(
            BookMove("e4", "The classical first move: centre plus two pieces freed."),
            BookMove("e5", "Black meets it head on."),
            BookMove("Nf3", "Develops with a threat against e5."),
            BookMove("Nc6", "The natural defence."),
            BookMove("Bb5", "The Spanish bishop. It does not threaten to win e5 yet — the knight on c6 is pinned only loosely — but it asks Black a question that lasts all game."),
            BookMove("a6", "The Morphy Defence, and the most useful move in the opening: it forces the bishop to declare its intentions, and gains the b5 square for later."),
            BookMove("Ba4", "Retreating but keeping the diagonal. The bishop still eyes c6 and can drop back to b3 to hit f7.",
                     (("Bxc6", "The Exchange Variation. Playable, but giving up the bishop pair to fix Black's pawns is a strategic commitment, not a free win."),)),
            BookMove("Nf6", "Develops and hits e4 — Black must generate counterplay, not just defend."),
            BookMove("O-O", "White ignores the e4 pawn. If 6...Nxe4 7.Re1 pins and regains it; king safety is worth more than a tempo here."),
            BookMove("Be7", "Modest but correct. Black prepares to castle and unpins nothing prematurely."),
            BookMove("Re1", "Defending e4 properly and putting the rook on the file that will open."),
            BookMove("b5", "Kicking the bishop before White's pressure on e5 becomes real."),
            BookMove("Bb3", "The bishop lands on its permanent home, aimed at f7 through the coming middlegame."),
            BookMove("d6", "Shoring up e5 so the knight on c6 is free to move."),
            BookMove("c3", "Preparing d4, the standard central break. White has spent the opening arranging one pawn push."),
            BookMove("O-O", "Both kings are safe and the real game begins. This position has been played tens of thousands of times."),
        ),
        plans=(
            "White: manoeuvre the b1 knight via d2-f1-g3 to the kingside — the famous 'Spanish knight' route.",
            "White: play d4 at the right moment, when Black cannot answer with a comfortable ...exd4.",
            "Black: counterattack on the queenside with ...Na5 and ...c5, using the space b5 and a6 bought.",
        ),
    ),
    Line(
        key="scotch",
        name="Scotch Game",
        eco="C45",
        hero=W,
        summary=(
            "White resolves the central tension immediately instead of "
            "manoeuvring. A practical choice: far less theory than the Ruy "
            "Lopez, and it leads to open positions where pieces matter more "
            "than memorised moves."
        ),
        moves=(
            BookMove("e4", "Centre and development."),
            BookMove("e5", "Symmetrical reply."),
            BookMove("Nf3", "Hits e5."),
            BookMove("Nc6", "Defends it."),
            BookMove("d4", "The Scotch. White strikes at once rather than preparing with c3."),
            BookMove("exd4", "Effectively forced — leaving the tension allows dxe5 with an edge."),
            BookMove("Nxd4", "Recapturing with the knight, which now sits actively in the centre."),
            BookMove("Bc5", "Black develops with a threat against the knight on d4, gaining time.",
                     (("Nf6", "The other main move, leading to the sharp 5.Nxc6 bxc6 6.e5 lines. Sound, but far more forcing."),)),
            BookMove("Be3", "Defending the knight with a piece rather than retreating it. Development and defence in one move."),
        ),
        plans=(
            "White: castle queenside in some lines and attack down the g- and h-files.",
            "White: the c3/f3 pawn structure supports the knight and blunts Black's dark-squared bishop.",
            "Black: pressure d4 and aim for the ...d5 break to free the position.",
        ),
    ),
    Line(
        key="friedliver",
        name="Two Knights Defence: Fried Liver Attack",
        eco="C57",
        hero=W,
        summary=(
            "The most instructive attack a beginner can learn: White sacrifices "
            "a knight to drag the black king into the open on move six. Learn "
            "it from both sides — you need to know how to play it *and* how to "
            "avoid walking into it."
        ),
        moves=(
            BookMove("e4", "Centre."),
            BookMove("e5", "Centre."),
            BookMove("Nf3", "Attacks e5."),
            BookMove("Nc6", "Defends e5."),
            BookMove("Bc4", "Aiming at f7."),
            BookMove("Nf6", "The Two Knights. Black develops and counterattacks e4 rather than mirroring with ...Bc5."),
            BookMove("Ng5", "Breaking the 'do not move a piece twice' rule — legitimately. Two attackers now hit f7 and Black has only the king defending it."),
            BookMove("d5", "The only good answer: block the bishop's diagonal by counterattacking in the centre.",
                     (("Bc5", "The Traxler, a wild counter-gambit. Enormous fun and enormous risk — not a first repertoire."),
                      ("Nxe4", "Loses to 5.Bxf7+ Ke7 6.d4, when Black's king is stuck in the middle and White is simply better."))),
            BookMove("exd5", "Accepting. White opens the position with Black's king still on e8."),
            BookMove("Nxd5", "The natural recapture — and the mistake. Black should play 5...Na5, giving up a pawn to chase the bishop.",
                     (("Na5", "The correct move! It attacks the bishop on c4 and sidesteps the whole attack. If your opponent finds this, respect it and play 6.Bb5+ with a normal game."),)),
            BookMove("Nxf7", "The Fried Liver. White gives a knight to force the king out — with the queen, bishop and remaining knight all ready to join in."),
            BookMove("Kxf7", "Forced. Declining loses the exchange and the position."),
            BookMove("Qf3+", "The follow-up that makes the sacrifice work: check, and a second attacker on the pinned knight on d5."),
            BookMove("Ke6", "The only move that holds the knight. The black king stands on the sixth rank on move seven — which is why this attack is famous."),
            BookMove("Nc3", "Bringing the last piece in with tempo against d5. White has full compensation and a raging initiative."),
        ),
        plans=(
            "White: every move must come with a threat — the moment the attack pauses, Black consolidates a piece up.",
            "White: target the pinned d5 knight; it is the glue holding Black's position together.",
            "Black (defending): remember 5...Na5! and none of this happens. Prevention beats defence.",
        ),
    ),
    Line(
        key="scholars",
        name="Refuting Scholar's Mate",
        eco="C20",
        hero=B,
        summary=(
            "Not an opening so much as an inoculation. The four-move mate is "
            "the most common way beginners lose, and the refutation teaches "
            "the real lesson: an early queen raid loses time when met calmly."
        ),
        moves=(
            BookMove("e4", "White's most popular first move."),
            BookMove("e5", "The classical reply."),
            BookMove("Bc4", "Aimed at f7 — so far, a perfectly good developing move."),
            BookMove("Nc6", "Develop normally. Do not panic; nothing is wrong yet."),
            BookMove("Qh5", "The threat: Qxf7# — the queen takes, protected by the bishop on c4. Two attackers, one defender."),
            BookMove("g6", "The refutation. It blocks the queen's path to f7 *and* attacks her, so Black gains a tempo while defending.",
                     (("Nf6", "The losing move — 4.Qxf7# is mate. The knight defends h5 and d5, but not f7, and the king cannot take because the bishop on c4 guards the square."),
                      ("Qe7", "Defends f7 but blocks Black's own bishop and leaves the queen badly placed. Playable, passive, and unnecessary."))),
            BookMove("Qf3", "White keeps aiming at f7. The queen has now moved twice and been chased once.",
                     (("Qxe5+", "Grabbing the pawn with check, but after 4...Qe7! the queens come off and White's whole plan has achieved nothing."),)),
            BookMove("Nf6", "Develops, covers d5, and shields the position. Black is now simply better: three pieces developed against White's queen sortie."),
        ),
        plans=(
            "Black: finish developing — ...Bg7, ...O-O — and White's queen will have to retreat, having lost three tempi.",
            "Black: the g6/Bg7 setup is a genuinely good structure, not just a defensive concession.",
            "General: when attacked early, look for the move that defends *and* threatens. Pure defence hands over the initiative.",
        ),
    ),
    # ------------------------------------------------------------ e4 others
    Line(
        key="sicilian",
        name="Sicilian Defence, Najdorf Variation",
        eco="B90",
        hero=B,
        summary=(
            "The most successful answer to 1.e4 ever devised, and the sharpest. "
            "Black declines symmetry from move one and plays for a win with "
            "the black pieces. Demands real study — this is the entry point."
        ),
        moves=(
            BookMove("e4", "White takes the centre."),
            BookMove("c5", "The Sicilian. Black attacks d4 from the side rather than occupying the centre — and crucially, trades a wing pawn for White's centre pawn, giving an extra central pawn and an open c-file."),
            BookMove("Nf3", "White's most testing move, preparing d4."),
            BookMove("d6", "Controlling e5 so that White's d4 push cannot be followed by e5 with tempo. It also opens the c8 bishop's diagonal."),
            BookMove("d4", "White strikes. This is the Open Sicilian — the critical test."),
            BookMove("cxd4", "Black takes, completing the central trade the Sicilian is built on."),
            BookMove("Nxd4", "White recaptures with the knight, which sits well but can be challenged."),
            BookMove("Nf6", "Developing with a hit on e4, forcing White to defend rather than build."),
            BookMove("Nc3", "The natural defence of e4."),
            BookMove("a6", "The Najdorf move, and it looks like nothing. It takes b5 away from White's pieces permanently, and prepares ...e5 or ...b5 depending on what White commits to. It is a *waiting* move with concrete purpose.",
                     (("g6", "The Dragon — also excellent, but it invites a direct race after Be3/Qd2/O-O-O and h4-h5. A different kind of game."),
                      ("Nc6", "The Classical. Sound, but it commits the knight before Black knows where it belongs."))),
        ),
        plans=(
            "Black: the half-open c-file is the main asset — a rook on c8 pressures c3 and c2 all game.",
            "Black: strike with ...e5 or ...b5 at the right moment; the whole point of ...a6 is keeping both options.",
            "Black: expect opposite-side castling and a mutual race. Count tempi, not material.",
            "White: the standard try is 6.Be3 followed by f3, Qd2, O-O-O and a kingside pawn storm.",
        ),
    ),
    Line(
        key="french",
        name="French Defence, Winawer Variation",
        eco="C18",
        hero=B,
        summary=(
            "Black builds a solid pawn chain and accepts a cramped but very "
            "sturdy position, then attacks White's centre at its base. The "
            "Winawer is its sharpest form."
        ),
        moves=(
            BookMove("e4", "White claims the centre."),
            BookMove("e6", "Quiet but committal: it prepares ...d5 so that Black can challenge e4 immediately, backed by a pawn.",),
            BookMove("d4", "White builds the full centre, as invited."),
            BookMove("d5", "The point. Black attacks e4 with a pawn — White must resolve the tension."),
            BookMove("Nc3", "Defending e4 and developing. The most testing choice.",
                     (("e5", "The Advance Variation — White grabs space, and Black gets the classic plan of ...c5 and ...Nc6 hitting the base at d4."),
                      ("exd5", "The Exchange Variation. Symmetrical and drawish; it releases all the central tension for nothing."))),
            BookMove("Bb4", "The Winawer. Black pins the knight defending e4, so the threat of ...dxe4 becomes real. It is committal — the bishop will usually be exchanged, giving White the bishop pair for damaged pawns."),
        ),
        plans=(
            "Black: the light-squared bishop on c8 is the problem piece — every good French plan has an answer for it.",
            "Black: attack d4, the base of White's chain, with ...c5 and ...Nc6.",
            "Black: after ...Bxc3+ bxc3, White's doubled c-pawns are a long-term target.",
            "White: use the space advantage and the bishop pair to attack on the kingside.",
        ),
    ),
    Line(
        key="carokann",
        name="Caro-Kann Defence, Classical Variation",
        eco="B18",
        hero=B,
        summary=(
            "The French's solid cousin, without the bad bishop. Black plays "
            "...c6 first so that after ...d5 the light-squared bishop can get "
            "out to f5 before the pawn chain locks it in. Extremely reliable."
        ),
        moves=(
            BookMove("e4", "White takes the centre."),
            BookMove("c6", "Preparing ...d5 with a pawn behind it — the same idea as the French, but keeping the c8 bishop's diagonal open. That single difference defines the opening."),
            BookMove("d4", "White builds the big centre."),
            BookMove("d5", "Challenging e4 on Black's terms."),
            BookMove("Nc3", "Defending e4."),
            BookMove("dxe4", "Releasing the tension. Black is content to trade and develop smoothly rather than fight for space."),
            BookMove("Nxe4", "White recaptures with the knight."),
            BookMove("Bf5", "The whole point of 1...c6. The bishop reaches an active square *outside* the pawn chain — the piece that suffers in the French is Black's best piece here."),
        ),
        plans=(
            "Black: the structure is rock-solid; aim for ...e6, ...Nd7, ...Ngf6 and a comfortable game.",
            "Black: play for the endgame — the pawn structure is healthier than White's in many lines.",
            "White: chase the bishop with Ng3 and gain space with h4-h5 before Black consolidates.",
        ),
    ),
    # -------------------------------------------------------------- d4 lines
    Line(
        key="qgd",
        name="Queen's Gambit Declined",
        eco="D35",
        hero=B,
        summary=(
            "The most respectable answer to 1.d4. Black declines the pawn and "
            "builds a solid centre, accepting a slightly passive bishop in "
            "exchange for a position that is very hard to break down."
        ),
        moves=(
            BookMove("d4", "The other great first move — it takes the centre with a pawn that is already defended by the queen."),
            BookMove("d5", "Black meets it symmetrically, staking the same claim."),
            BookMove("c4", "The Queen's Gambit. Not a true gambit: White offers the c-pawn to deflect Black's d-pawn from the centre, and can regain it whenever they wish."),
            BookMove("e6", "Declining, and the soundest way to do it. Black supports d5 with a pawn so the centre holds.",
                     (("dxc4", "The Queen's Gambit Accepted — fully playable, but Black must not try to hold the pawn. See the 'qga' line."),
                      ("c6", "The Slav — equally sound, and it keeps the c8 bishop's diagonal open. See the 'slav' line."))),
            BookMove("Nc3", "Adding a third attacker to d5 and developing."),
            BookMove("Nf6", "Defending d5 a second time and developing toward the centre."),
            BookMove("Bg5", "Pinning the knight, so the pressure on d5 becomes real again."),
            BookMove("Be7", "Calmly breaking the pin's sting. Black now threatens to castle and unravel.",
                     (("Nbd7", "Playable but concrete: it invites 5.cxd5 exd5 6.Nxd5?! Nxd5 7.Bxd8 Bb4+! — the Elephant Trap, winning a piece back with interest."),)),
        ),
        plans=(
            "Black: the c8 bishop is the problem piece. Solve it with ...b6 and ...Bb7, or ...dxc4 followed by ...b5.",
            "Black: aim for the ...c5 break, which frees the position in one move.",
            "White: the minority attack — push b4-b5 on the queenside to create a weak pawn on c6.",
        ),
    ),
    Line(
        key="qga",
        name="Queen's Gambit Accepted",
        eco="D20",
        hero=B,
        summary=(
            "Black takes the pawn and gives up the centre for fast development "
            "and free play. The essential lesson: take the pawn, but never try "
            "to keep it."
        ),
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("d5", "Black matches."),
            BookMove("c4", "The gambit offer."),
            BookMove("dxc4", "Accepted. Black concedes the centre in return for a tempo and easy piece play."),
            BookMove("e3", "The solid recapture plan — White will take on c4 with the bishop next move.",
                     (("e4", "Grabbing the whole centre. Ambitious and sharp, and Black hits back at once with 3...e5 or 3...Nf6."),)),
            BookMove("Nf6", "Developing and controlling the centre from a distance. Black does *not* try to hold c4.",
                     (("b5", "The losing greed. 4.a4! c6 5.axb5 cxb5 6.Qf3! forks the rook on a8 and the pawn on b5 — Black loses material. This is the single most important thing to know about the QGA."),
                      ("Be6", "Trying to guard c4 with a piece. It blocks the e-pawn and after 4.Na3 the pawn falls anyway, with Black underdeveloped."))),
            BookMove("Bxc4", "White regains the pawn, as was always available. Material is level and both sides have a normal game."),
            BookMove("e6", "Opening the f8 bishop and preparing to castle. Black's position is free and easy to play."),
        ),
        plans=(
            "Black: play ...c5 to hit d4 and complete equality — this break is the whole strategy.",
            "Black: ...a6 and ...b5 gains queenside space and chases the bishop on c4.",
            "White: the extra central pawn means more space; use it to build a kingside initiative.",
        ),
    ),
    Line(
        key="slav",
        name="Slav Defence",
        eco="D15",
        hero=B,
        summary=(
            "Support d5 with the c-pawn instead of the e-pawn, and the "
            "light-squared bishop keeps its freedom. Solid enough for world "
            "championship matches, simple enough to learn quickly."
        ),
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("d5", "Black matches."),
            BookMove("c4", "The Queen's Gambit."),
            BookMove("c6", "The Slav. It defends d5 like ...e6 does, but leaves the c8-h3 diagonal open — solving the problem piece of the Queen's Gambit Declined before it becomes one."),
            BookMove("Nf3", "Developing and controlling e5."),
            BookMove("Nf6", "Mirroring, and defending d5 again."),
            BookMove("Nc3", "The third attacker on d5."),
            BookMove("dxc4", "Now the capture makes sense: with ...c6 played, Black can meet a4 with ...b5 supported, and ...Bf5 develops the bishop actively."),
        ),
        plans=(
            "Black: develop the bishop to f5 or g4 *before* playing ...e6 — that is the entire point of the Slav.",
            "Black: ...b5 supported by ...a6 holds the extra pawn far better than in the QGA.",
            "White: play e4 to seize the centre while Black spends time on the queenside.",
        ),
    ),
    Line(
        key="kid",
        name="King's Indian Defence",
        eco="E60",
        hero=B,
        summary=(
            "Black lets White build the biggest centre they like, fianchettoes, "
            "castles, and then attacks it. A hypermodern opening: control the "
            "centre with pieces first, occupy it later."
        ),
        moves=(
            BookMove("d4", "White takes the centre."),
            BookMove("Nf6", "Controlling e4 with a piece instead of a pawn — the hypermodern idea in one move."),
            BookMove("c4", "White grabs more space."),
            BookMove("g6", "Preparing the fianchetto. The bishop on g7 will aim at d4 and the long diagonal for the rest of the game."),
            BookMove("Nc3", "Supporting the coming e4."),
            BookMove("Bg7", "The most important piece in the opening. Everything Black does is built around this bishop's diagonal."),
            BookMove("e4", "White has the ideal classical centre — and Black has *let* them, on purpose."),
            BookMove("d6", "Restraining e5 and preparing the thematic ...e5 break. Black's position looks passive and is anything but."),
        ),
        plans=(
            "Black: play ...e5, let White close with d5, then attack on the kingside with ...f5, ...f4, ...g5, ...g4.",
            "Black: in the closed structure, ignore the queenside entirely — it is a pure race and the king is the target.",
            "White: attack on the queenside with c5 and a minority push; the side with more space on a wing attacks there.",
            "Warning: the KID loses badly when played passively. It is an attacking opening disguised as a defence.",
        ),
    ),
    Line(
        key="london",
        name="London System",
        eco="D02",
        hero=W,
        summary=(
            "The same setup against almost anything Black plays: d4, Bf4, e3, "
            "Nf3, c3, Bd3, Nbd2. Minimal theory, maximum reliability — the "
            "practical choice when you would rather spend study time on "
            "endgames than on move 18 of a sideline."
        ),
        moves=(
            BookMove("d4", "The foundation of the setup."),
            BookMove("d5", "Black's most common reply, though the London plays much the same against most moves."),
            BookMove("Bf4", "The defining move. Getting the bishop *outside* the pawn chain before playing e3 — do this in the wrong order and the bishop is buried for the whole game.",
                     (("e3", "The move-order error. After 2.e3 the c1 bishop is locked behind its own pawns and the London has already failed."),)),
            BookMove("Nf6", "Black develops naturally."),
            BookMove("e3", "Only now does the pawn go to e3, supporting d4 and opening the f1 bishop. The bishop on f4 is already safely outside the chain."),
            BookMove("e6", "Black mirrors the solid setup."),
            BookMove("Nf3", "Completing the kingside development."),
            BookMove("c5", "Black's standard challenge to the d4 pawn."),
            BookMove("c3", "The quiet answer that holds everything together: d4 is defended, and the queen gets the c2 square to link the bishop on d3 with the kingside."),
        ),
        plans=(
            "White: Bd3, Nbd2, O-O, then Ne5 — the knight on e5 is the attacking piece in every London game.",
            "White: after Ne5, play f4 to support it and build a slow kingside attack.",
            "White: Qc2 lines up queen and bishop at h7. That battery is the most common way a London game is won.",
            "Weakness to know: Black playing an early ...c5 and ...Qb6 hits b2 and d4 at once — meet it with Qb3 or Nc3.",
        ),
    ),
)


# --- Indexes ---------------------------------------------------------------
BY_KEY: Dict[str, Line] = {line.key: line for line in LINES}


def get(key: str) -> Optional[Line]:
    return BY_KEY.get(key.strip().lower())


def for_side(hero: Color) -> List[Line]:
    return [line for line in LINES if line.hero is hero]


def matching(played: List[str]) -> List[Line]:
    """Every book line that begins with the moves `played`.

    Used by explore mode to say "you are still in the Italian" — and, when the
    list empties, to say exactly which move left the book.
    """
    from .san import normalize

    want = [normalize(s) for s in played]
    out = []
    for line in LINES:
        sans = [normalize(s) for s in line.sans]
        if len(want) <= len(sans) and sans[: len(want)] == want:
            out.append(line)
    return out


def next_moves(played: List[str]) -> List[Tuple[Line, BookMove]]:
    """The book's continuations after `played`, one per matching line."""
    depth = len(played)
    seen, out = set(), []
    for line in matching(played):
        if depth < len(line.moves):
            book_move = line.moves[depth]
            if book_move.san not in seen:
                seen.add(book_move.san)
                out.append((line, book_move))
    return out
