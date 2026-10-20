# Real-Time Collaborative Editing

| | |
| --- | --- |
| **Tier** | 3 — if you have time |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 · [IGotAnOffer](https://igotanoffer.com/en/advice/openai-system-design-interview) (senior-level example) |
| **Most recent report** | 2026-03-11 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design real-time collaborative document editing like Google Docs.

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

**The crux:** OT vs CRDT and why; a server that sequences operations per document; presence and cursors; persistence as an operation log plus periodic snapshots; offline edits that merge on reconnect.

**Good clarifying questions:**
- Document size, editors per document, offline support, rich text vs plain text.

**Deep-dive menu:**
- OT transform functions vs CRDT metadata cost
- Per-document sequencer and its failover
- Snapshotting and history

**Follow-ups to expect:**
- Two users type at the same position.
- A user edits offline for an hour.
- 500 simultaneous editors.

**Traps:**
- Last-write-wins on the whole document.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
