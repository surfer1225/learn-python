# CI/CD System (GitHub Actions from Scratch)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×5 · [Hello Interview](https://www.hellointerview.com/guides/openai/l5) top-5 (Staff) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) · [Interview Query](https://www.interviewquery.com/interview-guides/openai-software-engineer) |
| **Most recent report** | 2026-05-26 |
| **ShowOffer video** (watch after your attempt) | [Design a CI/CD System](https://www.youtube.com/watch?v=y32PywFi7Ek) |
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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Runner fleet cost: autoscaling with spot capacity and job preemption.
- An untrusted PR from a fork runs a workflow — what isolation keeps secrets safe?
- Change the workflow YAML schema without breaking millions of repositories.
- Multi-region scheduler: where is the source of truth for job state?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
