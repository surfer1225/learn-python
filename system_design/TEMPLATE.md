# OpenAI System Design — Answer Template

Every question in [`openai/`](openai/) uses this template. Copy the section
headings, fill them in under a timer, then open the question's
**Interviewer notes** to grade yourself.

## Why this shape

The template is built around what candidates consistently report about the
OpenAI round, not a generic "requirements → boxes → scale" recipe:

| What OpenAI interviewers do | What the template forces you to do |
| --- | --- |
| 60-minute collaborative working session; they add constraints mid-way | Time-boxed phases with explicit check-ins |
| Expect **full stack** — wireframe, API contract, schema — not just a backend diagram | A dedicated *Client & API* phase before any boxes |
| Rarely say what to focus on; one candidate was told to treat model serving as a black box | A *Black-box list* in the first 5 minutes |
| Push scale hard: "what breaks at 100×? at 1000×?" | A *10× / 100× / 1000×* table naming the first thing to break |
| Ask how the tech you named works inside (Kafka rebalancing, WebSocket limits, K8s scheduling) | *Justify every component* — name it only if you can explain its internals |
| Probe failure: node crash, duplicate delivery, region loss, bad deploy | A *Failure modes* table you fill in before being asked |
| Reward clean MVP-first designs; some prompts are "small team, two-week MVP" | *v1 first*, then evolve — never open with hyperscale |

## Time budget (60 min)

| # | Phase | Minutes | Output on the board |
| --- | --- | --- | --- |
| 1 | Clarify & scope | 0–5 | One-sentence restatement · black-box list · interviewer sign-off |
| 2 | Requirements & estimates | 5–12 | Must / Should / Won't · non-functional numbers · back-of-envelope |
| 3 | Client & API | 12–20 | Wireframe + UI states · endpoints with request/response |
| 4 | Data model | 20–25 | Entities · keys · partition key · indexes · consistency per entity |
| 5 | High-level design v1 | 25–35 | Diagram · one request walked end to end |
| 6 | Scale & failure | 35–50 | 10× / 100× / 1000× table · failure-mode table |
| 7 | Deep dive | 50–58 | Two or three levels deep on one component |
| 8 | Wrap-up | 58–60 | Trade-offs made · what you'd do next |

For a 45-minute round, cut phase 3 to 5 minutes and phase 7 to 5 minutes.

## The sections

### 1. Clarify & scope
- Restate: **"So we are designing ___ that ___, optimizing for ___."**
- Ask questions that show judgment ("I'd assume X because Y — OK?"), not "what
  should I build?".
- Write the **black-box list**: what you will *not* design (usually model
  inference, auth, billing). Get a nod before moving on.

### 2. Requirements & estimates
- **Functional:** Must (MVP) / Should / Won't. Keep Must to 3–5 items.
- **Non-functional with numbers:** users, QPS (avg and peak), latency targets
  (p50/p99), durability, availability, delivery guarantee
  (at-most / at-least / effectively-once), consistency per operation.
- **Back-of-envelope:** only the numbers that change a decision (storage per
  year, peak write QPS, fan-out, egress). Say what each number decides.

### 3. Client & API
- ASCII **wireframe** of the main screen, plus the states users see: loading,
  streaming, empty, error, offline, retrying.
- **Endpoints:** method, path, request, response, status codes. Mark which are
  idempotent and how (idempotency key, PUT semantics).
- **Transport:** REST / SSE / WebSocket / gRPC — and why for *this* product.

### 4. Data model
- Core entities with primary keys and the fields that matter.
- **Partition key** and the access pattern it serves. Secondary indexes.
- Which store and **why** (consistency, access pattern, scale), and what
  consistency each entity needs.

### 5. High-level design v1
- The simplest design that meets the Must list at stated scale.
- Draw it, then **walk one request end to end**, naming every hop.

### 6. Scale & failure
| Load | What breaks first | Redesign |
| --- | --- | --- |
| 10× | | |
| 100× | | |
| 1000× | | |

| Failure | Detection | Behaviour / recovery | User sees |
| --- | --- | --- | --- |
| Node / worker crash | | | |
| Duplicate or out-of-order message | | | |
| Dependency slow or down | | | |
| Region outage | | | |
| Bad deploy | | | |

### 7. Deep dive
- Offer a **menu** of 2–3 components; let the interviewer pick.
- Go two or three levels down: data structures, concurrency, the exact
  failure sequence, the numbers.

### 8. Wrap-up
- Trade-offs you made and what would make you revisit them.
- Observability: the 3–5 metrics and alerts that tell you it's healthy.
- What you'd build next with more time.

## Self-grading rubric

Score each 1–4 after every attempt (4 = what a strong senior/staff hire does).

| Axis | 2 — weak | 4 — strong |
| --- | --- | --- |
| **Scoping** | Starts drawing immediately | Restates, sets black-box list, gets sign-off, checks in throughout |
| **Full stack** | Backend boxes only | Wireframe, precise API contract, schema that matches both |
| **Scale thinking** | "Add more servers" | Names the first bottleneck at each threshold and redesigns that part |
| **Correctness under failure** | Happy path only | Retries, idempotency, ordering, partial failure, user-visible behaviour |
| **Technical depth** | Names technologies | Explains internals and alternatives for every named component |
| **Simplicity** | Over-engineered from minute one | Clean v1, evolved only when a requirement forces it |
| **Communication** | Interviewer drives | You drive; trade-offs stated out loud as you go |

## Traps that recur across OpenAI reports

- Spending time on transformers, GPUs or training when nobody asked — treat
  inference as a black-box API unless told otherwise.
- Skipping the front end on a product prompt.
- Naming a technology you can't defend at the internals level.
- Promising "exactly-once" without explaining idempotency and dedup.
- Hyperscale on minute one instead of an MVP that evolves.
