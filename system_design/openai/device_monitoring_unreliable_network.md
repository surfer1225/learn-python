# Device Monitoring and Control over an Unreliable Network (Power Grid / IoT)

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×8 (incl. IoT logging) |
| **Most recent report** | 2026-09-28 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design a system to monitor and control power-grid devices — solar inverters, home batteries — that report telemetry and receive commands over the unreliable public internet.

**Reported variants:**

- Dedup and late events
- Command dispatch and telemetry reconciliation for unreliable devices
- IoT logging platform with late-arriving metrics
- Real-time electricity monitoring and policy control
- User-respecting smart-grid controller
- Power-plant system from an underspecified prompt

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

**The crux:** Assume at-least-once, out-of-order, late delivery. Devices buffer and resend, so dedupe on (device_id, sequence). Aggregate by event time with watermarks and accept corrections for late data. Don't fire and forget commands: keep a versioned desired state per device (a device shadow / digital twin), let the device acknowledge its reported state, and reconcile until the two match. Commands must be idempotent, expire, and respect the user's own constraints.

**Good clarifying questions:**
- Device count and report frequency; control latency target.
- Are device clocks trustworthy? Do devices have sequence numbers and local storage?
- What does "respect the user" mean — user constraints override grid policy?
- The prompt is underspecified on purpose: say what you'd ask first and why.

**Deep-dive menu:**
- Ingest: MQTT/HTTPS gateway → log partitioned by device_id → stream processor
- Dedup with a per-device high-water-mark sequence; idempotent writes
- Late data: event-time windows, watermarks, recomputing aggregates; time-series DB with downsampling tiers
- Command path: versioned desired state, device pulls/acks, retries with the same command id, TTL
- Liveness: heartbeats, offline detection, alerting without flapping

**Follow-ups to expect:**
- A device is offline for six hours, then dumps its backlog.
- Device clocks are skewed by minutes.
- A command is delivered twice. Does the battery discharge twice?
- A grid emergency must reach 1M devices within 30 seconds.

**Traps:**
- Assuming the network delivers exactly once.
- Processing-time windows.
- Fire-and-forget commands.

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- A bad command rollout could destabilise part of the grid. Staged rollout, blast-radius limits, kill switch.
- Regulators ask which command reached which device and when. Retention and audit design.
- Thirty device models with different protocols — where is the adapter boundary and who owns it?
- The prompt is underspecified: drive the scoping, and write the assumptions down as a contract the interviewer agrees to.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
