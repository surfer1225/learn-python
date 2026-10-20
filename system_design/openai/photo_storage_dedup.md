# Photo Storage with Content Deduplication

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×4 (incl. duplicate file detection) |
| **Most recent report** | 2026-09-20 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a photo storage service that deduplicates uploads by SHA-256 content hash and still supports safe deletion.

**Reported variants:**

- Content-addressed photo storage
- Duplicate file detection

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

**The crux:** Separate content-addressed blobs (keyed by hash) from user-facing photo records that reference them. The hard part is deletion: reference counting or mark-and-sweep GC with a grace period, and the race between a delete driving the count to zero and a concurrent upload of the same hash. Never trust a client-supplied hash, and note that cross-user dedup leaks whether a file exists.

**Good clarifying questions:**
- Dedup per user or across all users (privacy side-channel)?
- Exact duplicates only, or near-duplicates (perceptual hashing)?
- Photo size, upload volume, retention and legal-hold rules.

**Deep-dive menu:**
- Upload flow: presigned URL to staging, server-side hash, promote or link to existing blob
- Refcount in a transactional DB vs tombstone + delayed GC
- Resumable chunked uploads; thumbnails as derived blobs
- Storage tiering for cold photos

**Follow-ups to expect:**
- User A deletes while user B uploads the same photo.
- Should you worry about SHA-256 collisions?
- Dedup reveals that another user has a file.
- A stored blob is corrupted.

**Traps:**
- Trusting the client's hash.
- Deleting the blob immediately when a reference drops.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
