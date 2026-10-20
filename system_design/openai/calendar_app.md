# Multi-Device Calendar

| | |
| --- | --- |
| **Tier** | 3 — if you have time |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 |
| **Most recent report** | 2025-11-09 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a calendar application that syncs across devices: events, recurring events, invitations and reminders.

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

**The crux:** Event model with recurrence rules plus exceptions; time zones and DST; delta sync with sync tokens and offline edits; conflict resolution; reminder scheduling at scale.

**Good clarifying questions:**
- Offline editing? Shared calendars? Reminder precision?

**Deep-dive menu:**
- RRULE + exceptions storage
- Sync tokens and conflict handling
- Reminder scheduler

**Follow-ups to expect:**
- Edit "this and following" occurrences.
- Conflicting offline edits on two devices.
- 100M reminders at 9:00.

**Traps:**
- Materializing every occurrence of a recurring event forever.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
