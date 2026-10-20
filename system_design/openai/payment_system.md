# Payment System (Holds, Capture, Batch Settlement)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×17 · [Hello Interview](https://www.hellointerview.com/guides/openai/l5) top-5 (Staff) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) · [Interview Query](https://www.interviewquery.com/interview-guides/openai-software-engineer) |
| **Most recent report** | 2026-09-28 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design the payment system for a chain of coffee shops. A card is authorized when the customer pays, the tip is added later, the funds are captured, and everything is settled nightly in batches through an external payment provider.

**Reported variants:**

- Holds and captures, batch charges, reconciliation, idempotency
- Coffee-shop card payments with tips and nightly batch settlement at scale
- Payment processing with exactly-once charging
- Charge customers through an external payment provider
- Offline merchant payments with reconciliation
- Payment orchestration system; high-throughput authorization and settlement

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

**The crux:** Money must move exactly once even though the provider is unreliable and every network call can time out with an unknown outcome. That means: a per-payment state machine (authorized → tip-adjusted → captured → settled, plus voided/refunded), idempotency keys on every provider call, an immutable double-entry ledger as the source of truth, and a reconciliation job that compares the provider's settlement report against the ledger.

**Good clarifying questions:**
- Who are we — the merchant, a gateway, or the processor? (Usually: the merchant's backend talking to Stripe/Adyen-like provider.)
- Card-present at a terminal, or online? Must terminals work offline (store-and-forward with risk limits)?
- Tip rules: max tip over the authorized amount? Authorization expiry window (≈7 days)?
- Settlement: daily cutoff time, per-merchant or global batches, what happens to items that fail in a batch?
- PCI scope — we store tokens, never PANs.

**Deep-dive menu:**
- Idempotency: client-generated key, stored with a request hash and the final response; same key + different body → 422
- Provider timeout → payment in UNKNOWN state → query provider by idempotency key before retrying
- Transactional outbox so the ledger write and the provider call can't diverge
- Nightly batch: cutoff snapshot, sharded by merchant, checkpointed, re-runnable without double-submitting
- Reconciliation: match provider settlement file to ledger; classify mismatches; correcting entries, never edits

**Follow-ups to expect:**
- The provider returns 500 but actually charged the card. What now?
- A terminal is offline for four hours. What do you accept, and what is your risk?
- The customer taps twice. How do you avoid charging twice?
- How do you guarantee a voided authorization never lands in tonight's batch?
- Why a relational database here and not a NoSQL store? What isolation level?

**Traps:**
- Floats for money (use integer minor units + currency).
- Updating a balance column in place with no ledger.
- Claiming Kafka gives exactly-once end to end.
- Retrying a non-idempotent provider call blindly.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
