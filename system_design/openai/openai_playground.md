# OpenAI Playground

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×3 · [Aced](https://www.aced.io/blog/openai-system-design-interview) (phone screen) |
| **Most recent report** | 2026-04-25 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design the OpenAI Playground: a developer tool to experiment with prompts and model settings, simulate full conversations, save and manage threads and presets, and export the result as API code.

**Reported variants:**

- ChatGPT Playground
- AI playground editor
- Minimal ChatGPT with presets

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

**The crux:** Front-end heavy: candidates were asked for wireframes, the API layer and the thread/message schema, and one was told to prioritize the front end. Get the editor state right (draft vs saved, autosave, versioned presets), stream through an API layer that enforces the org's quota, and make Stop actually cancel upstream so the user isn't billed.

**Good clarifying questions:**
- Individual developers only, or org sharing of presets?
- Do presets need version history? Side-by-side model comparison?
- Is model serving a black box? (One candidate was told yes.)
- Code export: which languages, and does it include the conversation?

**Deep-dive menu:**
- Autosave and multi-tab edits: optimistic concurrency with a version number
- Preset versioning: immutable versions + a pointer to latest; diff between versions
- Streaming + Stop: AbortController on the client → cancel the upstream request → stop billing
- Client-side token counting and cost estimate before sending
- Per-org rate limits and key management in the API layer

**Follow-ups to expect:**
- The same preset is open in two tabs and both edit it.
- The user hits Stop. Are tokens after that point billed?
- Show a diff between two preset versions.
- Scale to 1M developers.

**Traps:**
- No wireframe.
- Ignoring cancellation and billing.
- Designing model serving when the interviewer wanted the product.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
