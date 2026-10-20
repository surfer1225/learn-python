# Metrics Monitoring and Alerting

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 · [Interview Query](https://www.interviewquery.com/interview-guides/openai-software-engineer) |
| **Most recent report** | 2026-10-01 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a metrics monitoring and alerting system like Datadog or Prometheus: collect metrics from many services, store time series, power dashboards and fire alerts. Go deep on one or two components.

**Reported variants:**

- Metrics monitoring system, going deep on one or two components

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

**The crux:** Ingestion (push vs pull), time-series storage (compression, label index, cardinality limits), downsampling and retention tiers, a query engine for dashboards, and an alert evaluator that is highly available without paging twice. The prompt explicitly asks for depth over breadth.

**Good clarifying questions:**
- Number of active series, resolution, retention.
- Dashboard query latency; multi-tenant?

**Deep-dive menu:**
- Cardinality explosion and how to cap it
- Write path sharded by series hash; compression (delta-of-delta, XOR)
- Late samples
- HA alerting with deduplicated notifications and flap suppression

**Follow-ups to expect:**
- A team adds a user_id label.
- A network partition — do alerts still fire?
- Who monitors the monitor?

**Traps:**
- One row per data point in a relational DB.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
