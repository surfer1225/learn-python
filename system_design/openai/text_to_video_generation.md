# Text-to-Video Generation Service (Sora-style)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×10 |
| **Most recent report** | 2026-09-28 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a Sora-style text-to-video service. Users submit prompts; each generation takes minutes on one GPU; users see progress and can cancel. Free and paid tiers share a limited GPU fleet, and traffic bursts after launches.

**Reported variants:**

- GPU job scheduler with one GPU per task and fair queueing
- Fair queueing and cancellation
- GPU scheduling, failures, traffic bursts
- Tier-aware generation service
- Asynchronous / fault-tolerant video generation orchestration

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

**The crux:** This is an async job system over a scarce, expensive resource. The model is a black box `generate(prompt) -> video` on a GPU worker. What's graded: admission control, fair scheduling across tiers and users without starvation, worker leases so crashed jobs come back, cancellation that actually frees the GPU, results to object storage + CDN, and honest progress/ETA to the user.

**Good clarifying questions:**
- Job duration distribution and fleet size — how many GPUs, how many jobs per hour?
- SLA per tier: paid max wait? Can free jobs be preempted? Can jobs checkpoint?
- When the queue is too long: reject at submit, or accept with an ETA?
- Output size, retention, and how users get notified.

**Deep-dive menu:**
- Per-tier queues + weighted scheduler vs one priority queue (starvation); per-user concurrency caps
- Worker pull with lease + heartbeat (visibility timeout); idempotent job execution; retry budget
- Cancellation: status flag the worker polls between steps vs kill signal; release the GPU, refund quota
- Burst handling: admission control, ETA from queue depth × p50 duration, preempting free tier
- Progress: worker reports steps to a status store; clients poll or subscribe via SSE

**Follow-ups to expect:**
- Traffic goes 10× after a launch tweet. What do free and paid users each experience?
- A GPU node dies at 90% of a 5-minute job.
- One free user submits 500 jobs.
- How do you show queue position cheaply for 100k waiting jobs?
- How do you keep GPU utilization high while staying fair?

**Traps:**
- Holding an HTTP request open for minutes.
- Using Kafka as a work queue without discussing per-job ack, retries and head-of-line blocking.
- Strict priority with no starvation story.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- The GPU fleet is fixed for the quarter. Turn fairness into knobs leadership can tune (tier weights, quotas) and the metrics that show their effect.
- A new model version is 2× slower and runs on a mixed fleet. How do you route, roll out, and roll back?
- Make cost per generated second a first-class metric. Where is it measured and how does it feed scheduling?
- Where do prompt and output moderation sit, and what happens when a job is blocked halfway through?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
