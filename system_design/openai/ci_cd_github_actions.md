# CI/CD System (GitHub Actions from Scratch)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×5 · [Hello Interview](https://www.hellointerview.com/guides/openai/l5) top-5 (Staff) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) · [Interview Query](https://www.interviewquery.com/interview-guides/openai-software-engineer) |
| **Most recent report** | 2026-05-26 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design GitHub Actions from scratch: a multi-tenant CI/CD system where repositories define workflows triggered by events, jobs run on isolated runners, and users watch logs live.

**Reported variants:**

- Multi-tenant CI/CD platform for many orgs
- CI/CD pipeline with a scheduler
- Stuck-job handling
- Live log streaming
- Build caching

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

**The crux:** Event (webhook) → workflow parsed into a DAG of jobs → scheduler with per-tenant fairness and quotas → runners that pull and lease jobs with heartbeats → artifacts and caches in object storage → logs streamed live and finalized to blob storage. Stuck jobs are handled with lease expiry and timeouts, and retries are idempotent.

**Good clarifying questions:**
- Hosted runners, self-hosted, or both? (Self-hosted behind NAT forces a pull model.)
- Isolation level for hosted runners; secrets handling.
- Scale: jobs per minute, peak after a monorepo push; matrix builds.
- Log retention and live-view expectations.

**Deep-dive menu:**
- DAG/job state machine in a DB; leasing via SELECT … FOR UPDATE SKIP LOCKED or a queue with visibility timeout
- Stuck jobs: heartbeat miss vs job timeout vs user cancel — and how each is cleaned up
- Live logs: runner uploads chunks, viewers subscribe over SSE, finalized to blob storage
- Build cache keyed by hash of inputs (lockfile), scoped per branch, eviction policy
- Multi-tenancy: per-org concurrency limits, fair scheduling, secret masking in logs

**Follow-ups to expect:**
- A runner dies mid-job.
- A monorepo push triggers 5,000 jobs.
- A secret leaks into a log line.
- The same webhook is delivered twice.
- A viewer opens the log of a running job vs a finished one.

**Traps:**
- Pushing jobs to runners without a lease.
- Storing logs in the relational database.
- No tenant isolation or fairness.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
