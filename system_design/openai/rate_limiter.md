# Distributed Rate Limiter

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 · [Interview Query](https://www.interviewquery.com/interview-guides/openai-software-engineer) |
| **Most recent report** | 2026-05-11 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a distributed rate limiter for an API such as the OpenAI API: limit each API key on requests per minute and tokens per minute, enforced across many gateway nodes.

**Reported variants:**

- Distributed rate limiter

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

**The crux:** Pick an algorithm and say why (token bucket vs sliding-window counter vs log). Keep state in a central store with atomic updates (Redis + Lua) within a tight latency budget. Decide fail-open vs fail-closed. Tokens per minute are only known after the response, so reserve an estimate up front and reconcile afterwards.

**Good clarifying questions:**
- Dimensions: per key, per org, per model? Requests and tokens?
- Accuracy vs added latency; global or per region?
- Behaviour when the limiter store is down.

**Deep-dive menu:**
- Redis cluster sharded by key; atomic check-and-decrement
- Local token caches for hot keys with periodic sync
- Response headers: Retry-After, remaining, reset
- Multi-region limits

**Follow-ups to expect:**
- Redis is down.
- One key sends 50k requests per second.
- A streamed response uses more tokens than estimated.
- Clocks differ across gateways.

**Traps:**
- Per-node limits only.
- Fixed windows without mentioning boundary bursts.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
