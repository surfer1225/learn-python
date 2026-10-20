# Usage Credits and Quotas

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×3 |
| **Most recent report** | 2026-05-03 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a credit and quota system for model usage: orgs buy or are granted credits (GPU-hours or tokens) that expire; every request draws down the balance; usage must never go meaningfully negative.

**Reported variants:**

- GPU credit allocator
- Credit balance with vector-clock expirations
- Mobile model usage quotas

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

**The crux:** A ledger of grants (each with its own expiry) and debits; consume earliest-expiring credit first; the balance is derived and cached. The tension is strong consistency vs request-path latency at high QPS. Reserve-then-settle, lease budget slices to gateways or regions, and bound the overdraft you accept. Debits must be idempotent.

**Good clarifying questions:**
- Hard limit or soft limit? Acceptable overdraft?
- Debit QPS for the biggest org; multi-region writes?
- Mobile clients offline?

**Deep-dive menu:**
- Hot-org contention: sharded counters, budget leases to gateways
- Expiry: background job vs computing lazily at read time
- Multi-region: CRDT-style counters / vector clocks with bounded overdraft
- Audit trail and refunds

**Follow-ups to expect:**
- Two regions debit the same org at the same moment.
- A grant expires in the middle of a request.
- Refund a failed request.
- Month-end usage report.

**Traps:**
- One balance row updated on every request at 100k QPS.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
