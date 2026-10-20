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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Account deletion under GDPR when blobs are shared, backed up and cached at the CDN.
- Cost model: dedup ratio vs metadata overhead — when is dedup not worth it?
- Migrate an existing 10 PB non-deduplicated store to content addressing online.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
