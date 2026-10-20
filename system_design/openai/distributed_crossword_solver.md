# Distributed Crossword Solver

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×6 |
| **Most recent report** | 2026-05-12 |
| **ShowOffer video** (watch after your attempt) | [Design a Crossword Puzzle Solver](https://www.youtube.com/watch?v=bEGs-PUTAWg) |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a distributed system that fills crossword grids: given a grid and a large dictionary, find valid fills, spreading the search across many machines.

**Reported variants:**

- Distributed crossword fill solver
- Crossword puzzle solver system / solving service

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

**The crux:** Nail the single-machine algorithm first: constraint satisfaction with backtracking, choosing the most-constrained slot next, and a word index by (length, position, letter) for fast pattern matching. Then distribute: split the search tree into work units, coordinate workers with leases, rebalance skewed subtrees with work stealing, stop everyone when a solution is found, and detect termination when there is none.

**Good clarifying questions:**
- One valid fill, all fills, or the best-scoring fill?
- Grid sizes and dictionary size.
- One very hard puzzle (latency) or many puzzles per second (throughput)?
- Is this a user-facing service with submissions and results?

**Deep-dive menu:**
- Word index: bitsets per (length, position, letter) intersected for pattern matches
- Splitting: expand the frontier to N subproblems; dynamic splitting / work stealing for skew
- Coordinator: leases, heartbeats, cancellation broadcast on first solution
- Termination detection when no solution exists
- Caching solved grids; replicating the dictionary to workers

**Follow-ups to expect:**
- One subtree is 1,000× bigger than the rest.
- A worker dies holding a lease.
- How do you know the search is finished?
- Serve 10k small puzzles per second vs one 25×25 grid.

**Traps:**
- Jumping to distribution before the algorithm is clear.
- Static partitioning only.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Generalise into a constraint-search platform (crosswords, Sudoku, scheduling). What is the API?
- When is distributing slower or costlier than one big machine? Show the math.
- Speculative parallel work is wasted work — how do you bound it and measure it?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
