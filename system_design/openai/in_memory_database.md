# In-Memory Key-Value Database

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×4 |
| **Most recent report** | 2025-08-04 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design an in-memory key-value database with get/set/delete, TTLs and transactions (begin/commit/rollback); then make it durable and distributed.

**Reported variants:**

- In-memory database API
- In-memory key-value database

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

**The crux:** Often starts as coding and grows into design. Core structures (hash map, TTL via lazy + sampled expiry), nested transactions as a stack of undo logs, durability via write-ahead log + snapshots with an fsync policy, replication (leader/follower, sync vs async), sharding by consistent hashing, and eviction when memory is full.

**Good clarifying questions:**
- Single node or distributed? How much data loss on crash is acceptable?
- Value types; nested transactions?
- Read/write ratio and consistency for replica reads.

**Deep-dive menu:**
- Nested transaction semantics and rollback
- Snapshot without pausing writes (fork + copy-on-write, or MVCC)
- Failover, split brain and fencing
- Hot keys and eviction policy (LRU vs LFU)

**Follow-ups to expect:**
- Crash in the middle of a write.
- Memory is full.
- A read from a lagging replica.
- 10× more keys.

**Traps:**
- Expiring TTLs by scanning every key.
- Replication without a story for split brain.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
