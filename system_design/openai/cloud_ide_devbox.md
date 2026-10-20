# Cloud IDE / Devbox Service

| | |
| --- | --- |
| **Tier** | 1 — must prepare |
| **Reported by** | [PracHub](https://prachub.com/companies/openai/categories/system-design) ×14 (incl. hosted notebooks) |
| **Most recent report** | 2026-10-12 |
| **ShowOffer video** (watch after your attempt) | [Design Cloud IDE with Remote Devboxes](https://www.youtube.com/watch?v=uuH2CIZUXxM) |
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

**L5 (staff) push — where a senior answer stops and a staff answer keeps going:**
- Idle workspaces are 60% of spend. Design the policy and the mechanism to cut it without anyone losing work.
- Roll out a host-kernel security patch to 10k hosts that are running workspaces.
- Other teams want the sandbox layer for notebooks, CI and code-executing agents. Where is the platform boundary and what is its API?
- Capacity planning: warm hosts per region per hour — who owns the forecast and what happens when it's wrong?

</details>

## Attempt log

| Date | Minutes | Rubric (scope / stack / scale / failure / depth / simple / evolve / comms) | Gaps to fix |
| --- | --- | --- | --- |
| | | | |
