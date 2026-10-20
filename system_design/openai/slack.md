# Slack (Team Messaging)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×6 · [Aced](https://www.aced.io/blog/openai-system-design-interview) (phone screen and onsite) · [Hello Interview](https://www.hellointerview.com/guides/openai/l4) (two-week MVP) · [Coditioning](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) |
| **Most recent report** | 2026-04-26 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design Slack: workspaces, channels, DMs, real-time message delivery, presence and history. Variant: you're a small team with a two-week MVP deadline — what do you build?

**Reported variants:**

- Multi-tenant global messaging
- High-scale chat app (Slack / WhatsApp / Teams), hundreds of millions of users
- Team chat system
- Two-week MVP for a small team

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

**The crux:** A persistent-connection tier (WebSocket gateways), a message service that writes to a durable store with per-channel ordering, and fan-out to online members via pub/sub keyed by channel. Offline clients catch up with a cursor. Presence is ephemeral soft state, never in the primary DB. Workspaces are the natural shard. For the MVP variant the grade is what you cut and why.

**Good clarifying questions:**
- Workspace size range (10 vs 100k members); biggest channel.
- Ordering guarantee: per channel only?
- Edits, threads, reactions, files, search — which are MVP?
- Single region or global?

**Deep-dive menu:**
- Per-channel sequence numbers; client gap detection and fetch-on-gap
- Fan-out: gateways subscribe to channels of their connected users; huge channels fan out on read
- Presence: heartbeat + TTL, subscribe only for users on screen
- Storage: Postgres for the MVP vs Cassandra/DynamoDB partitioned by (channel_id, time bucket)
- Connection tier: per-host limits, reconnect storms after deploy, jittered backoff

**Follow-ups to expect:**
- Two-week MVP with three engineers: exactly what ships?
- A gateway deploy drops 1M connections at once.
- A channel with 200k members gets an announcement.
- A client sees messages out of order.
- One workspace spans three regions.

**Traps:**
- Polling the database for new messages.
- Global message ordering.
- Presence writes to the primary database.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
