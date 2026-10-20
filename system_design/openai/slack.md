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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- From the two-week MVP, which decisions must be right on day one to avoid a rewrite (ID scheme, ordering, tenancy key), and which are disposable?
- Enterprise customers require data residency and customer-managed keys. What changes in storage and fan-out?
- Search over a ten-year workspace: indexing pipeline, permission filtering, reindexing when channel membership changes.
- Reconnect storm after a regional failover — capacity and admission control.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
