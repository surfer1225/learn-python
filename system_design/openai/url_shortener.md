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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Malware and phishing scanning pipeline with takedown SLAs.
- Thirteen months of click analytics — storage cost.
- Custom domains for enterprise customers: TLS certificates at scale.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
