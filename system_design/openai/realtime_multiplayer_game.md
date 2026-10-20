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

## 2. Requirements & estimates (5–12 min)

**Must:**
-

**Should:**
-

**Won't:**
-

**Non-functional (with numbers):**
-

**Back-of-envelope (and what each number decides):**
-

## 3. Client & API (12–20 min)

**Wireframe and UI states:**

```text

```

**Endpoints:**

| Method | Path | Request | Response | Idempotent? |
| --- | --- | --- | --- | --- |
| | | | | |

**Transport and why:**

## 4. Data model (20–25 min)

| Entity | Key / partition key | Key fields | Store and why |
| --- | --- | --- | --- |
| | | | |

## 5. High-level design v1 (25–35 min)

```text

```

**One request, end to end:**
1.

## 6. Scale & failure (35–50 min)

| Load | What breaks first | Redesign |
| --- | --- | --- |
| 10× | | |
| 100× | | |
| 1000× | | |

| Failure | Detection | Behaviour / recovery | User sees |
| --- | --- | --- | --- |
| | | | |

## 7. Deep dive (50–58 min)

**Menu I'd offer:**
-

**Chosen and notes:**

## 8. Wrap-up (58–60 min)

**Trade-offs and what I'd do next:**
-

**Metrics and alerts:**
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

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
