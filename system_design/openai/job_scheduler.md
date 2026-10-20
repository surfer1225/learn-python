# Distributed Job Scheduler

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [Aced](https://www.aced.io/blog/openai-system-design-interview) (phone screen) · related: GPU job schedulers in [text-to-video](text_to_video_generation.md) |
| **Most recent report** | — |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a distributed job scheduler: users submit one-off or cron jobs that must run at a given time on a worker fleet, with retries and status visibility.

**Reported variants:**

- Distributed task orchestration, fault tolerance and scaling

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

**The crux:** A durable job store, a time-indexed trigger that finds due jobs without double-firing (partitioned schedulers or leader election), dispatch to a queue, workers that lease jobs and heartbeat, at-least-once execution with idempotent jobs, and an explicit policy for missed fires.

**Good clarifying questions:**
- Precision: seconds or minutes? Jobs per second at peak (midnight)?
- Job duration; dependencies between jobs (DAG)?
- Overlap policy for cron jobs whose previous run is still going.

**Deep-dive menu:**
- Finding due jobs: DB poll with SKIP LOCKED vs timing wheel vs delayed queue
- Sharding scheduler ownership by job-id hash; failover
- Cron next-run computation across DST and time zones
- Leases and heartbeats for long-running jobs

**Follow-ups to expect:**
- A scheduler node dies at 11:59:59 with jobs due at 12:00.
- 1M jobs are due at midnight.
- A job runs twice. How harmful is that, and how do you prevent it?
- A job must never overlap its previous run.

**Traps:**
- A single cron box.
- No lease, so crashed jobs vanish or run twice.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
