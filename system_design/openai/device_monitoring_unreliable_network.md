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

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
