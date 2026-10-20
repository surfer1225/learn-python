# News Feed (Instagram)

| | |
| --- | --- |
| **Tier** | 3 — if you have time |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×1 |
| **Most recent report** | 2026-05-25 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design an Instagram-like feed: users follow others, post photos, and see a ranked, paginated feed.

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

**The crux:** Fan-out on write vs on read, with a hybrid for celebrities; media served via CDN; cursor pagination; ranking as a separate stage.

**Good clarifying questions:**
- Follower distribution; freshness target; ranked or chronological.

**Deep-dive menu:**
- Hybrid fan-out
- Feed cache structure
- Handling deletes and privacy changes

**Follow-ups to expect:**
- A celebrity with 300M followers posts.
- A post is deleted after fan-out.

**Traps:**
- Pure fan-out on write for every account.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
