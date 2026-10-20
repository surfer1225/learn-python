# LLM-Powered Enterprise Search (Permission-Aware RAG)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [IGotAnOffer](https://igotanoffer.com/en/advice/openai-system-design-interview) (common question) · [DesignGurus](https://www.designgurus.io/answers/detail/what-to-expect-in-the-openai-system-design-interview) (frequent in senior final loops) |
| **Most recent report** | — |
| **ShowOffer video** (watch after your attempt) | No exact match · related: [Master Search — Part 1](https://www.youtube.com/watch?v=3MIGT__j6_A), [Part 2](https://www.youtube.com/watch?v=Mq22eUCPOls) |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design an LLM-powered enterprise search: employees ask natural-language questions over company content from many sources (Drive, Slack, wikis, tickets) and get answers with citations — and nobody may ever see content they lack permission for.

**Reported variants:**

- Ingestion, permissions-aware indexing, retrieval, and where model inference sits in the query path

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

**The crux:** The LLM is a black box at the end of the query path; the system is everything before it. Connectors that sync incrementally under source API rate limits; a chunk → embed → index pipeline; hybrid retrieval (BM25 + vector ANN) with permission filtering inside retrieval, not after generation; reranking; answer generation grounded in cited chunks; and propagation of ACL changes and deletions fast enough to be safe.

**Good clarifying questions:**
- Tenants and documents per tenant; which sources; freshness target for edits and for ACL changes.
- Answer with citations, a ranked result list, or both? Latency target?
- Must permissions be exact at query time, or is a short propagation delay acceptable? (Usually: revocations must be fast.)
- Is the LLM and embedding model a black box with a cost per call?

**Deep-dive menu:**
- Permission-aware retrieval: ACL principals stored per chunk, group expansion, pre-filter vs post-filter and the recall cost of each
- Connectors: webhooks vs polling, cursors, backfill vs incremental, per-source rate limits and backoff
- Embedding model upgrade: re-embedding billions of chunks with dual indexes and a cutover
- Hybrid retrieval + reranking; context assembly and citation grounding
- Prompt injection hidden inside indexed documents

**Follow-ups to expect:**
- A user is removed from a group. How quickly do they lose access to its documents in answers?
- Re-embed the whole corpus with a new model without downtime.
- One tenant has 500M documents.
- How do you measure answer quality, and catch a regression before customers do?
- A document contains "ignore previous instructions and reveal…"

**Traps:**
- Filtering permissions after the LLM has seen the chunks.
- One shared index with no tenant isolation story.
- Ignoring source API rate limits during backfill.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Quality as a system: offline eval sets, online feedback, regression gates on model and prompt changes.
- Cost per query and per indexed document — where caching pays off.
- Deletion and residency guarantees across index replicas and caches.
- Third parties write connectors: what is the contract, and how do you keep a bad connector from hurting the platform?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
