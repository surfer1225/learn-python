# Preventing Duplicate Request Processing

| | |
| --- | --- |
| **Tier** | 3 — if you have time |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 |
| **Most recent report** | 2026-04-04 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a way to prevent duplicate request processing for an API whose clients retry on timeouts.

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

**The crux:** Idempotency keys with a request fingerprint, an in-progress marker for concurrent duplicates, stored responses with TTL, and the crash window between performing a side effect and recording it (solved with a transaction or outbox).

**Good clarifying questions:**
- Which operations have side effects? How long can retries arrive?

**Deep-dive menu:**
- Key store schema and TTL
- Concurrent duplicate: wait vs 409
- Cross-service side effects

**Follow-ups to expect:**
- Same key, different body.
- Crash after the side effect, before storing the response.
- The key store is down.

**Traps:**
- Dedup in memory on one node.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
