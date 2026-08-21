# Backend SWE Interview Prep — 12-Week Study Plan

Interview-ready for **senior backend** roles: Python · Algorithms & Data
Structures · Backend Engineering · System Design · Modern AI Infrastructure.

**Study time:** weekdays 2–3 h/day · weekends 4–6 h/day (~18–24 h/week).

> This plan merges the 12-week roadmap with what already exists in this repo.
> **Status:** `[ ]` todo · `[x]` done · 🎬 has a visual aid in `experiments/`.
> Solve a stub, then run the file (e.g. `python arrays/two_sum.py`) — it prints
> `ok` when the self-checks pass.

---

## How to use this plan (daily loop)
1. **Warm-up (15 min):** re-solve one *already-solved* problem from memory (spaced repetition — this is what makes patterns stick).
2. **Main block:** the week's focus below.
3. **Explain out loud:** narrate your approach as if to an interviewer *before* coding. Communication is graded as heavily as the solution at senior level.
4. **End of day:** commit; update the Progress line at the bottom.

**Guiding principle — interleave, don't silo.** Even in System Design weeks, keep 2–3 algo reps/week so retention doesn't decay. Start light mock interviews by Week 4, not just Week 12.

---

## Success criteria
- [ ] Idiomatic Python: type hints, dataclasses, generators, context managers, `asyncio`.
- [ ] Solve mediums confidently and most hards, **explaining reasoning throughout**.
- [ ] Build production components from scratch: cache, rate limiter, scheduler, queue, pub/sub, in-memory DB.
- [ ] Design scalable distributed systems; discuss performance / reliability / consistency / cost trade-offs.
- [ ] Explain AI-app infra: tokenization, embeddings, vector search, retrieval (RAG), streaming APIs, conversation memory.
- [ ] Tell 6–8 crisp behavioral stories (STAR) covering conflict, failure, leadership, ambiguity.

---

## Phase 0 — Environment & tooling (1 day)
- [x] Python 3.13 + VS Code + Git + virtualenv (`.venv/`)
- [x] Project structure + auto-commit hook (`.claude/settings.local.json`)
- [ ] `pip install black ruff pytest mypy pre-commit`
- [ ] Add `pyproject.toml` (configure black/ruff/mypy) + `.pre-commit-config.yaml` so format+lint+type-check run on every commit
- [ ] `pytest` wired so `tests/` runs green (chess tests already pass)

> Want this scaffolded? Say the word and I'll add `pyproject.toml`, pre-commit, and move the ad-hoc `__main__` self-checks into `tests/`.

---

## Phase 1 — Python mastery (Weeks 1–2)
Write Python like an experienced backend engineer.

- [ ] Core data structures cold: `list`, `dict`, `set`, `tuple`, `collections` (`deque`, `defaultdict`, `Counter`, `OrderedDict`), `heapq`
- [ ] Idioms: comprehensions, generators/`yield`, unpacking, `enumerate`/`zip`, f-strings
- [ ] Typing: `Optional`, `Generic`/`TypeVar`, `Protocol`, `dataclass` (`frozen`, `slots`)
- [ ] OOP & protocols: dunders, ABCs, `__slots__`, name mangling (`_`/`__`)
- [ ] Functional tools: `functools` (`lru_cache`, `partial`, `reduce`), `itertools`
- [ ] Context managers (`with`, `contextlib`), decorators, error handling
- [ ] Concurrency primer: threads vs `asyncio` vs multiprocessing, the GIL
- **Already in repo:** 🎬 `experiments/pi_simulation.py` (generators), `chess/` (clean OOP package), `design/lru_cache.py` (generics, dataclass, typing).
- **Milestone:** add 2–3 `experiments/` files (decorators, `dataclass`, `asyncio`) that each demonstrate one feature.

---

## Phase 2 — Algorithms & data structures (Weeks 3–5)

**The full question bank lives in [QUESTIONS.md](QUESTIONS.md)** — 144 problems
across 15 patterns, each a runnable stub with the statement, a worked example,
and self-checks.

Every pattern folder is split by priority:

| Tier | Meaning | Count |
| --- | --- | --- |
| **Tier 1** | Must prepare — the core set | 60 |
| **Tier 2** | Good to prepare — common follow-ups | 56 |
| **Tier 3** | Prepare if you have time — hard or niche | 28 |

```
arrays/tier1/two_sum.py          # topic first, then tier
graphs/tier2/rotting_oranges.py
```

**Order:** finish **Tier 1 across every pattern** before starting Tier 2.
Breadth beats depth for interview coverage, and the patterns reinforce each
other. Tier 3 is for after Tiers 1–2 are solid.

**Patterns:** Arrays & Hashing · Two Pointers · Sliding Window · Stack ·
Binary Search · Linked List · Trees · Tries · Heap · Backtracking · Graphs ·
Dynamic Programming · Intervals · Greedy · Math & Bits.

**Per-question loop** (the sequencing is the skill, not just the answer):
1. State the approach, its time/space complexity, and *why it is correct* —
   before writing a line of code.
2. Name the alternative approach and why you are not taking it.
3. Then code it. Run the file; it prints `ok` when the assertions pass.
4. Write the complexity into the function docstring. If you cannot, you have
   not finished.

- **Milestone (end Week 5):** all 60 Tier 1 problems solved, each with a
  complexity docstring; can re-derive any of them cold in <15 min while
  narrating.

---

## Phase 3 — Production coding (Weeks 6–8)
Build real backend components from scratch (`design/`, `concurrency/`).

- [x] **LRU Cache** — `design/lru_cache.py` 🎬 (interview + production variant: TTL, `get_or_load`, stats, thread-safe)
- [x] **LFU Cache** — `design/lfu_cache.py`
- [ ] **Rate limiter** — token bucket + sliding-window log (`design/rate_limiter.py`)
- [ ] **Task scheduler** — delayed/periodic jobs on a heap (`design/scheduler.py`)
- [ ] **Thread-safe queue / producer–consumer** (`concurrency/`)
- [ ] **Pub/Sub** — topics, subscribers, backpressure (`design/pubsub.py`)
- [ ] **In-memory key-value store** — TTL, optional persistence (`design/kv_store.py`)
- [ ] **Search index / inverted index** (`design/inverted_index.py`)
- [ ] Concurrency deep-dive: `threading.Lock`/`RLock`, `queue.Queue`, `concurrent.futures`, `asyncio` event loop
- **Milestone:** each component has tests, type hints, and a docstring on complexity & trade-offs.

---

## Phase 4 — System design (Weeks 9–10)
Design scalable distributed systems; always state trade-offs.

- [ ] Fundamentals: latency vs throughput, CAP, consistency models, back-of-envelope estimation
- [ ] Building blocks: load balancing, caching (write-through/back, eviction), consistent hashing, sharding, replication
- [ ] Storage: SQL vs NoSQL, indexing, partitioning; queues & streaming (Kafka)
- [ ] Reliability: idempotency, retries, circuit breakers, rate limiting, observability
- [ ] **Design drills** (write notes in `system_design/`): URL shortener, rate limiter service, news feed, chat, distributed cache, web crawler, notification system
- **Milestone:** 5–7 written designs; can whiteboard any in 45 min with trade-offs.

---

## Phase 5 — Modern AI infrastructure (Week 11)
Backend building blocks behind AI apps.

- [ ] Tokenization & context windows; embeddings (what/why)
- [ ] Vector databases & similarity search (cosine, ANN/HNSW)
- [ ] Retrieval-Augmented Generation (RAG) pipeline end to end
- [ ] Streaming APIs (SSE/token streaming), latency & cost trade-offs
- [ ] Conversation memory / context management, prompt/response caching
- [ ] *build:* a tiny in-memory vector store + cosine top-k retriever (`experiments/` or `design/`)
- **Milestone:** explain a RAG system's data flow and where each backend concern (cache, queue, DB, rate limit) fits.

---

## Phase 6 — Mock interviews (Week 12)
- [ ] 4–6 timed coding mocks (45 min, explain throughout)
- [ ] 3–4 system design mocks (45 min)
- [ ] 1–2 behavioral rounds (STAR stories)
- [ ] Retro after each: what to tighten (communication, edge cases, time management)
- **Milestone:** consistent, calm, well-communicated solutions under time pressure.

---

## Visual aids & experiments
- `python heap/quickselect_walkthrough.py` — quickselect (kth largest without a
  heap) one step at a time, with the discarded half shrinking each round 🎬
- `python heap/heapify_walkthrough.py` — heapify one step at a time, paused by
  default, with the executing line of code highlighted 🎬
- `python heap/heap_visualization.py` — animated binary heap / priority queue:
  tree and array views side by side, sift-up/sift-down narrated step by step 🎬
  (`--selftest` verifies the model headlessly)
- `python experiments/lru_cache_visualization.py` — animated LRU (hash map + DLL) 🎬
- `python experiments/doubly_linked_list_animation.py` — the DLL behind LRU 🎬
- `python experiments/pi_simulation.py` — Monte Carlo vs. Leibniz π

## Suggested weekly order
Wk0 tooling · Wk1–2 Python · Wk3–5 Algorithms (+start light mocks Wk4) · Wk6–8 Production coding · Wk9–10 System design · Wk11 AI infra · Wk12 Mocks.

## Progress
Algorithms: **2 / 144** (Tier 1: **2 / 60**)  ·  Production components: **2 / 8**
System designs: **0 / 7**  ·  Mocks done: **0**
_(update as you go)_
