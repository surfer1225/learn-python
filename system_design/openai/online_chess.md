# Online Chess

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×9 · [Hello Interview](https://www.hellointerview.com/guides/openai/l5) #1 most asked (Staff) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) |
| **Most recent report** | 2026-09-21 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design an online chess service: players are matched by rating, play real-time games with clocks, and spectators can watch. Start with launch scale and evolve it.

**Reported variants:**

- Elo matchmaking, WebSocket moves, game clocks
- Fault-tolerant online chess service
- From launch to scale
- Matchmaking and clocks

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

**The crux:** The server is authoritative for game state and clocks. Each game has exactly one owner process at a time, with sticky routing, and every move is durably appended before it's acknowledged so a crashed owner can be rebuilt from the move log. Clocks must be fair under network latency. Matchmaking is a queue per time control with a rating window that widens with wait time. Spectator fan-out is separate from the players' path.

**Good clarifying questions:**
- Time controls — bullet (1+0) makes latency and clock fairness the core problem.
- Concurrent games at launch vs target; spectators per game (1 vs 100k for a top streamer).
- Anti-cheat in scope? Reconnect grace period?

**Deep-dive menu:**
- Matchmaking: buckets per time control, widening rating window, one matcher per bucket, avoiding double-matching
- Game owner: in-memory state, append move to a durable log before ack, game_id → server routing
- Clocks: server timestamps, RTT compensation, server-side flag detection
- Reconnect: client sends last seen move number; server replays the gap
- Spectators: pub/sub with small delay, fan-out tier separate from game servers

**Follow-ups to expect:**
- The game server crashes mid-game.
- A player's network drops for 10 seconds in a bullet game.
- Scale to 1M concurrent games.
- A modified client sends an illegal move.
- A player sits in two queues and gets matched twice.

**Traps:**
- Client-authoritative clocks.
- A database round trip per move with no latency discussion.
- One global matchmaking lock.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
