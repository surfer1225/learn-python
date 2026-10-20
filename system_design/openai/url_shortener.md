# URL Shortener

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×2 |
| **Most recent report** | 2026-01-19 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a URL shortener: create short links, redirect fast, support custom aliases and expiry, and record click analytics.

**Reported variants:**

- URL shortening service

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

**The crux:** ID generation (counter ranges + base62 vs hashing with collision handling), a read-heavy redirect path behind a cache, 301 vs 302 and what each does to analytics, and analytics captured asynchronously through a log/stream.

**Good clarifying questions:**
- Links created per day vs redirects per second.
- Custom aliases, expiry, analytics depth.

**Deep-dive menu:**
- Key generation service handing out ranges
- Enumeration and abuse; malicious targets
- Hot links and cache strategy

**Follow-ups to expect:**
- One link gets 100k redirects per second.
- Short codes are guessable.
- A short link points to malware.

**Traps:**
- Truncated hashes with no collision handling.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
