# Video Streaming Platform (Netflix)

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [Aced](https://www.aced.io/blog/openai-system-design-interview) (onsite) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) |
| **Most recent report** | — |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a video streaming platform at scale: ingest, transcoding, global delivery and playback, with user growth projected at 10× to 1000×.

**Reported variants:**

- Streaming platform at scale with variable frame rates and aggressive growth
- Design Netflix

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

**The crux:** Ingest → chunked parallel transcoding into an adaptive-bitrate ladder (HLS/DASH) → object storage → CDN with origin shield → player-side ABR. Egress through the CDN dominates cost and scale; the metadata service is small by comparison.

**Good clarifying questions:**
- VOD, live, or both? User-generated or curated catalog?
- Global audience? DRM?

**Deep-dive menu:**
- Transcoding DAG, retries, variable frame rates
- CDN hit ratio, prepositioning popular titles, origin shield
- ABR algorithm on the client
- Cost model and popularity skew

**Follow-ups to expect:**
- 1000× growth: what breaks first?
- A live event spike.
- A region outage.

**Traps:**
- Serving video bytes from application servers.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
