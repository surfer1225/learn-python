# Real-Time Multiplayer Game (Trivia Battle Royale)

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×2 |
| **Most recent report** | 2026-10-10 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a real-time trivia battle royale: thousands of players join a live game, answer timed questions, wrong answers eliminate players, and spectators watch live.

**Reported variants:**

- Trivia battle royale with live spectating
- Multiplayer typing race with typo freezes and fair matchmaking

---

## 1. Clarify & scope (0–5 min)

**Restate:** So we are designing ___ that ___, optimizing for ___.

**Questions I'd ask:**
-

**Black-box / out of scope:**
-

**The one or two hard problems this design lives or dies on:**
-

## 2. Requirements & estimates (5–10 min)

**Must:**
-

**Should:**
-

**Won't:**
-

**SLOs and non-functional numbers:**
-

**Back-of-envelope (and what each number decides):**
-

## 3. Client & API (10–17 min)

**Wireframe and UI states:**

```text

```

**Endpoints:**

| Method | Path | Request | Response | Idempotent? |
| --- | --- | --- | --- | --- |
| | | | | |

**Transport and why:**

## 4. Data model (17–22 min)

| Entity | Key / partition key | Key fields | Store and why |
| --- | --- | --- | --- |
| | | | |

## 5. High-level design v1 (22–32 min)

```text

```

**One request, end to end:**
1.

**Alternatives I rejected and why:**
-

## 6. Scale & failure (32–45 min)

| Load | What breaks first | Redesign |
| --- | --- | --- |
| 10× | | |
| 100× | | |
| 1000× | | |

| Failure | Detection | Behaviour / recovery | User sees |
| --- | --- | --- | --- |
| | | | |

## 7. Deep dive (45–55 min)

**Menu I'd offer:**
-

**Chosen and notes:**

## 8. Evolution & operations (55–60 min)

**v1 → v2 → v3, and how each migration happens without downtime:**
-

**Operating it — SLOs/alerts, rollout and rollback, top cost drivers, abuse and safety:**
-

**Ownership — which team owns which component, and the contracts between them:**
-

---

<details>
<summary><b>Interviewer notes</b> — open only after a timed attempt</summary>

**The crux:** Server-authoritative timing with a fair answer cutoff despite different latencies; broadcast fan-out of questions and fan-in aggregation of answers; a connection tier sized for the peak; spectators on a separate, slightly delayed path; and cheat resistance.

**Good clarifying questions:**
- Players per game; concurrent games.
- Is there prize money? (Sets how strict fairness must be.)
- Latency tolerance and spectator delay.

**Deep-dive menu:**
- Pre-send encrypted questions, release the key at T0 to equalize start
- Answer aggregation via sharded counters; elimination state
- Reconnect within a round
- Spectator fan-out like a broadcast/CDN tier

**Follow-ups to expect:**
- 1M players in one game.
- A player with 300 ms RTT.
- A connection node holding 50k players dies.

**Traps:**
- One server per game at 1M players.
- Trusting client timestamps.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Prize money brings regulators: every answer timestamp must be auditable.
- Host games for several partners on shared infrastructure — tenancy and isolation.
- Load-test a 1M-player game before the first real one.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
