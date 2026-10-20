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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- CDN strategy: build vs buy, multi-CDN steering, cost per GB as a top-line metric.
- Per-title encoding: when is re-encoding the back catalogue worth it?
- Live and VOD on one platform — what's shared and what isn't?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
