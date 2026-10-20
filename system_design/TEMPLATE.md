# OpenAI System Design — Answer Template (pitched at L5 / staff)

Every question in [`openai/`](openai/) uses this template. Fill the sections in
under a 60-minute timer, then open the question's **Interviewer notes** and
grade yourself with the rubric below.

**Target level.** Offer reports put OpenAI **L5 ≈ Meta E6 / IC6 (staff)**.
OpenAI interviews senior and staff candidates with the same rounds and sets
the level *after* the loop, and the design rounds and the project deep dive
weigh most in that decision. Candidates report that many people get downlevelled
coming in. So the same prompt is graded L4 or L5 by **how far past a correct
design you go** — that is what the staff layer in this template is for.

## Why this shape

| What OpenAI interviewers do | What the template forces you to do |
| --- | --- |
| 60-minute working session; they add constraints mid-way | Time-boxed phases with explicit check-ins |
| Expect **full stack** — wireframe, API contract, schema — not just a backend diagram | A *Client & API* phase before any boxes |
| Rarely say what to focus on; one candidate was told to treat model serving as a black box | A *black-box list* and the *hard problems* named in the first 5 minutes |
| Want you to **drive** — "learning to drive system design interviews is key" | You open each phase and propose the next; the interviewer reacts |
| Push scale hard: "what breaks at 100×? at 1000×?" | A 10× / 100× / 1000× table naming the first thing to break |
| Probe internals of whatever you name — down to file-descriptor limits when you colocate TCP connections | Name a technology only if you can explain how it works inside |
| Probe failure: crash, duplicate delivery, region loss, bad deploy | A failure table you fill in before being asked |
| At staff, expect long-term thinking: maintenance, evolution, operations | Section 8: *Evolution & operations* |

## Time budget (60 min)

| # | Phase | Minutes | Output on the board |
| --- | --- | --- | --- |
| 1 | Clarify & scope | 0–5 | Restatement · black-box list · **the 1–2 hard problems** · sign-off |
| 2 | Requirements & estimates | 5–10 | Must / Should / Won't · SLOs · back-of-envelope |
| 3 | Client & API | 10–17 | Wireframe + UI states · endpoints |
| 4 | Data model | 17–22 | Entities · keys · partition key · store and why |
| 5 | High-level design v1 | 22–32 | Diagram · one request end to end · rejected alternatives |
| 6 | Scale & failure | 32–45 | 10× / 100× / 1000× · failure table |
| 7 | Deep dive | 45–55 | Two or three levels down on one or two components |
| 8 | Evolution & operations | 55–60 | Roadmap and migrations · SLOs, rollout, cost, abuse · ownership |

A working v1 by minute 32 is what buys you the last 28 minutes, which is
where the staff signal lives. For a 45-minute round, shrink phases 3 and 7.

## The sections

### 1. Clarify & scope
- Restate: **"So we are designing ___ that ___, optimizing for ___."**
- Ask questions that show judgment ("I'd assume X because Y — OK?").
- Write the **black-box list** (usually model inference, auth, billing).
- **Name the hard problems out loud now** ("this lives or dies on
  exactly-once charging against an unreliable provider"). Seniors find the
  crux during the deep dive; staff candidates say it in minute three and
  steer the hour towards it.

### 2. Requirements & estimates
- **Functional:** Must (3–5 items) / Should / Won't.
- **SLOs with numbers:** availability, p50/p99 latency, durability, delivery
  guarantee, consistency per operation, freshness.
- **Back-of-envelope:** only numbers that change a decision — and say which
  decision each one changes.

### 3. Client & API
- ASCII **wireframe** plus the states users see: loading, streaming, empty,
  error, offline, retrying.
- **Endpoints** with request/response and status codes; mark idempotency.
- **Transport** (REST / SSE / WebSocket / gRPC) and why for *this* product.

### 4. Data model
- Entities, keys, the **partition key** and the access pattern it serves.
- Store choice and **why**; consistency each entity needs.

### 5. High-level design v1
- Simplest design that meets the Must list at stated scale.
- Walk **one request end to end**.
- **Rejected alternatives:** at least one real fork in the road ("pull vs
  push", "SQL vs wide-column") with the reason. Staff answers show the
  option space, not just the pick.

### 6. Scale & failure
- For each load step, the **first** thing to break, with the number that
  breaks it, and the redesign of only that part.
- Failure table: detection, recovery behaviour, what the user sees.

### 7. Deep dive
- Offer a menu; go two or three levels down: data structures, concurrency,
  exact failure sequences, numbers. Expect to be asked to sketch code.

### 8. Evolution & operations (the staff layer)
- **Roadmap:** v1 → v2 → v3 tied to growth or new requirements, and **how
  each migration runs without downtime** (dual writes, backfill, shadow
  reads, cutover, rollback).
- **Operating it:** SLOs and the alerts behind them; rollout and rollback;
  top two cost drivers and the lever for each; abuse, safety and privacy
  (deletion, residency).
- **Ownership:** which team owns which component and the contracts between
  them; what you'd make a platform for other teams.

## Self-grading rubric

Score each axis 1–4. L4 is a solid hire at senior; L5 is what gets you the
staff level.

| Axis | L4 (senior) | L5 (staff) |
| --- | --- | --- |
| **Scope** | Clarifies requirements, agrees scope | Names the hard problems up front and steers the hour to them; drives every phase |
| **Full stack** | Wireframe, API, schema present | Client states, API and schema consistent with each other and with the SLOs |
| **Scale** | Finds bottlenecks when pushed | Predicts the first bottleneck at each step with numbers before being asked |
| **Failure** | Handles crashes and retries | Reasons about partial failure, ordering, idempotency and what the user sees, unprompted |
| **Depth** | Explains internals of chosen components | Compares alternatives at the internals level and defends the choice for *these* constraints |
| **Simplicity** | Clean design | Clean v1 with a clear path to v3; knows what not to build |
| **Evolve & operate** | Mentions monitoring | Migration plan, rollout, SLOs, cost levers, ownership boundaries |
| **Communication** | Clear when asked | Thinks out loud, offers trade-offs, adapts smoothly when constraints change |

## Traps that recur across OpenAI reports

- Spending time on transformers, GPUs or training when nobody asked — treat
  inference as a black-box API unless told otherwise. (Infra-team loops are
  the exception: there, GPU scheduling, batching and cost are in scope.)
- Skipping the front end on a product prompt.
- Naming a technology you can't defend at the internals level.
- Promising "exactly-once" without explaining idempotency and dedup.
- Hyperscale on minute one instead of an MVP that evolves.
- At staff: a correct design that stops at the diagram, with no evolution,
  operations or ownership story.
