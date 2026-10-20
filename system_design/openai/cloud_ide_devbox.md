# Cloud IDE / Devbox Service

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×14 (incl. hosted notebooks) |
| **Most recent report** | 2026-10-12 |
| **Template** | [TEMPLATE.md](../TEMPLATE.md) |

## Prompt

> Design an online devbox service: users get on-demand cloud development environments they reach from a browser IDE or over SSH, edit and run code, stop them, and come back later to the same workspace.

**Reported variants:**

- Multi-tenant cloud IDE: isolation, workspaces, run/build, failure modes
- Cloud IDE with SSH access where one or more users share a host
- Sandboxed cloud IDE; IDE sandbox (paired with payments)
- Hosted notebook platform
- Cloud development environment platform like an online IDE

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

**The crux:** Separate the control plane (API, scheduler, workspace lifecycle state machine, reconciler) from the data plane (hosts running isolated workspaces, a connection proxy). The hard parts are isolation of untrusted code, persistence of workspace state across stop/start and host failure, fast start (warm pools, cached images), routing a browser/SSH connection to the right host, and reclaiming idle capacity because compute is the cost.

**Good clarifying questions:**
- Who runs code here — internal engineers or the untrusted public? (Decides containers vs gVisor vs Firecracker microVMs.)
- Persistent workspaces or ephemeral sandboxes? What must survive a stop: files only, or running processes?
- Resource shapes; GPUs? Start-time target (e.g. <10 s)?
- Multiple users in one workspace? Network egress policy?

**Deep-dive menu:**
- Workspace state machine (creating → running → stopping → stopped → archived) driven by a reconciliation loop
- Scheduler: bin-packing onto hosts, capacity headroom, warm pool sizing for the 9 am spike
- Storage: network block volume (AZ-bound, fast reattach) vs snapshot to object storage (portable, slow restore)
- Connection proxy: WebSocket for the IDE, SSH gateway with short-lived certs, routing table workspace → host
- Isolation and noisy neighbours: cgroups, seccomp, per-tenant network policy

**Follow-ups to expect:**
- A host with 40 running workspaces dies. What does each user lose, and how do they get back?
- Everyone opens their devbox at 9 am. How is start still under 10 seconds?
- A user runs a crypto miner or a fork bomb.
- How do you deploy the proxy without dropping every open terminal?
- How do you bill for this, and when do you shut idle boxes down?

**Traps:**
- "Just use Kubernetes" without explaining scheduling, storage and isolation.
- Shared-kernel containers for untrusted public code with no discussion.
- Ignoring cold-start time and idle cost.

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
