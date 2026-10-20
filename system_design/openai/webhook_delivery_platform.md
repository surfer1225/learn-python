# Webhook Delivery Platform

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [Hello Interview](https://www.hellointerview.com/guides/openai/l4) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) · [IGotAnOffer](https://igotanoffer.com/en/advice/openai-system-design-interview) · [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 (combined prompt) |
| **Most recent report** | 2025-07-04 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a webhook delivery platform: when events happen in our system, reliably deliver them via HTTP POST to endpoints our customers register.

**Reported variants:**

- Webhook callback system for third-party integrations
- Delivery failures are the centre of the question (Hello Interview L4)

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

**The crux:** At-least-once delivery to endpoints you don't control. Retries with exponential backoff and jitter; per-endpoint queues so one slow or dead endpoint can't block others; signed payloads (HMAC + timestamp) and a stable event id so consumers can dedupe; a dead-letter queue with replay; auto-disable and circuit breaking; SSRF protection on customer-supplied URLs.

**Good clarifying questions:**
- Event volume and fan-out (endpoints per event).
- Ordering requirement — none, or per resource key?
- Retry horizon (e.g. 3 days); delivery latency target.
- Do customers need a delivery log UI and manual replay?

**Deep-dive menu:**
- Producer side: transactional outbox so no event is lost
- Retry scheduling: delay queue vs DB table indexed on next_attempt_at vs timer wheel
- Isolation: per-endpoint concurrency caps, timeouts, fairness across tenants
- Security: HMAC signatures, replay window, blocking internal IP ranges
- Dead-lettering, replay, and auto-disabling chronically failing endpoints

**Follow-ups to expect:**
- An endpoint is down for two days, then recovers — the thundering herd.
- One customer is 90% of the volume.
- How does a customer verify a webhook really came from us?
- Replay last week's events for one customer.

**Traps:**
- Promising exactly-once delivery.
- One shared queue for every endpoint.
- No timeouts on outbound calls.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
