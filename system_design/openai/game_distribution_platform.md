# Digital Game Store and Distribution (Steam)

| | |
| --- | --- |
| **Tier** | 2 — good to prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×2 |
| **Most recent report** | 2026-09-18 |
| **ShowOffer video** (watch after your attempt) | None on the channel |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a digital game store and distribution platform like Steam: catalog, purchases and licenses, and fast downloads and updates of very large game files.

**Reported variants:**

- Digital game distribution platform

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

**The crux:** Purchase and licence correctness (a payments problem), delivery of 100 GB files via chunked, content-addressed manifests with delta patches over a CDN, launch-day spikes handled by pre-loading encrypted content and unlocking at release, and a read-heavy cached catalog.

**Good clarifying questions:**
- Concurrent downloads at a major launch; regions.
- DRM; mods or user content?

**Deep-dive menu:**
- Manifest + chunk design for delta updates and resume
- CDN capacity planning for release day
- Purchase idempotency and licence grant

**Follow-ups to expect:**
- 5M users download a 120 GB patch at release.
- Payment succeeded but the licence wasn't granted.
- Regional pricing.

**Traps:**
- Whole-file downloads for updates.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Release-day demand is 3× forecast. Pre-provisioning, CDN contracts, fallback.
- Chargebacks and stolen keys — where does fraud detection sit?
- Regional tax, pricing and age ratings without forking the catalogue.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
