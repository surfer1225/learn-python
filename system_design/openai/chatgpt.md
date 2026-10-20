# ChatGPT

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×8 · [Hello Interview](https://www.hellointerview.com/guides/openai/l5) top-5 (Staff) · [Educative](https://www.educative.io/courses/openai-system-design-interview-questions) · [rejected onsite, Jul 2026](https://prachub.com/interview-experiences/openai-software-engineer-interview-experience-chatgpt-system-design-vector-store-and-a-scheduler-debugging-round-rejected) |
| **Most recent report** | 2026-09-20 |
| **ShowOffer video** (watch after your attempt) | [Design ChatGPT](https://www.youtube.com/watch?v=5yHR1_2Y6bs) · background: [How LLM Inference Actually Works](https://www.youtube.com/watch?v=-7zk3XcZMGo) |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design ChatGPT: users have multi-turn conversations with a model, replies stream token by token, conversations are saved and listed in a sidebar, and free users have usage limits.

**Reported variants:**

- Streaming replies over SSE and rendering long conversations (asked: why SSE over WebSocket?)
- Chat assistant inference service: streaming, free-tier limits, GPU scheduling
- Highly available / reliable high-volume conversational AI service
- ChatGPT-like web chat UI; GPT chat UI with snapshots and sharing
- Large-scale streaming AI product feature

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

**The crux:** Full stack, not model internals. Client UI and rendering; a streaming transport you can justify (SSE: one-way, plain HTTP, reconnect with Last-Event-ID); conversation storage that is append-heavy and partitioned by user/conversation; context assembly to fit the window; an inference gateway that is a black box but owns routing, tier limits, queueing and backpressure; and what happens to a stream when the client disconnects.

**Good clarifying questions:**
- Is inference a black box? (Ask — the expected answer is usually yes.)
- Edit and regenerate (makes messages a tree, not a list)? Attachments? Share links?
- DAU, messages per user per day, average reply length in tokens.
- Free-tier quota rules, and what happens when the fleet is saturated.

**Deep-dive menu:**
- SSE vs WebSocket: direction of traffic, proxies/LB idle timeouts, HTTP/2 multiplexing, reconnect semantics
- Resumable streams: tokens buffered per message id (e.g. Redis stream) so reconnect resumes, generation continues server-side
- Message tree model for regenerate/edit; sharing as an immutable snapshot
- Long conversations: list virtualization, incremental markdown rendering, paginated history load
- Rate limiting by tokens/messages per window per tier; fallback model under overload

**Follow-ups to expect:**
- The user closes the tab mid-stream. Does generation continue? Is it billed?
- The load balancer kills idle connections at 60 s during a slow first token.
- Render a 2,000-message conversation smoothly.
- Someone shares a link while the conversation keeps going.
- A region goes down mid-stream.

**Traps:**
- Talking about transformers, KV caches or GPU kernels unprompted.
- Storing a conversation as one blob rewritten on every turn.
- No wireframe, no client states.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Chat must hit 99.95% while inference capacity is the scarce resource. Design degradation tiers: smaller model, queueing, shedding free traffic.
- Conversation storage grows by petabytes a year: retention, tiering, and deletion requests honoured across replicas and backups.
- Ship a new feature (memory, file uploads) without destabilising the core chat path — boundaries and ownership between teams.
- Data residency: where conversations live, and how a regional failover treats an in-flight stream.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
