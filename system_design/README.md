# System Design

## OpenAI question bank — targeting L5 (staff)

27 distinct questions, deduplicated from about 116 candidate-reported OpenAI
system design prompts plus the questions named in prep guides (compiled
2026-10-19).

| File | What it's for |
| --- | --- |
| [TEMPLATE.md](TEMPLATE.md) | The answer template every question uses, the 60-minute time budget, and the L4-vs-L5 rubric |
| [DEEP_DIVE.md](DEEP_DIVE.md) | Prep for the project presentation round, which weighs as much as design in the levelling decision |
| [`openai/`](openai/) | One file per question: prompt, reported variants, blank template, hidden interviewer notes with an **L5 push** section |

### What the L5 target means

- **Mapping.** Most offer reports put OpenAI **L5 ≈ Meta E6 / IC6** (e.g. a
  Meta E6 offered OpenAI L5, "directly equivalent to Meta E6" — Blind,
  Apr 2026). L6 is the next level up and L4 is a downlevel.
- **Level is set after the loop.** Senior and staff candidates get the same
  rounds; the design rounds and the project deep dive carry the most weight.
  One senior candidate: "They expect most people to downlevel coming in."
- **Typical loop** (varies by team — confirm with your recruiter):
  - Screen: 60 min coding + 60 min system design (Excalidraw), sometimes
    back to back. Some teams use a take-home instead.
  - Final, 4–6 hours: coding, a second system design, the project
    presentation, a senior-manager behavioural, a team-collaboration
    behavioural, and on some teams an agentic coding round.
- **The design bar at L5:** reach a coherent design within the hour, drive
  the conversation yourself, defend internals in depth (one follow-up went to
  file-descriptor limits), and cover maintenance, evolution and operations.
  [TEMPLATE.md](TEMPLATE.md) turns that into a section and a rubric.
- **Infra vs product teams.** Applied/product loops treat model inference as
  a black box. Platform, infra and SRE loops lean into GPU scheduling,
  batching, caching and cost — weight the GPU-heavy questions accordingly.

### L5 practice order

Do these timed at 60 minutes, in this order. Ordered by Hello Interview's
staff-level "most commonly asked" list, then report volume, then how much
staff-level depth the question invites.

1. [Payment System](openai/payment_system.md) — staff #2; most reported overall
2. [ChatGPT](openai/chatgpt.md) — staff #5; OpenAI's core product, degradation under scarce capacity
3. [CI/CD (GitHub Actions)](openai/ci_cd_github_actions.md) — staff #3
4. [Online Chess](openai/online_chess.md) — staff #1
5. [Slack](openai/slack.md) — staff #4; know the two-week MVP variant
6. [Text-to-Video Generation](openai/text_to_video_generation.md) — GPU scheduling depth; 10 reports
7. [Cloud IDE / Devbox](openai/cloud_ide_devbox.md) — 14 reports; isolation and platform boundaries
8. [Enterprise Search (RAG)](openai/enterprise_search_rag.md) — reported in senior final loops
9. [Webhook Delivery](openai/webhook_delivery_platform.md) — named in Hello Interview's L4 and L5 guides
10. [Device Monitoring](openai/device_monitoring_unreliable_network.md) — deliberately underspecified; tests scoping
11. [Job Scheduler](openai/job_scheduler.md) — phone-screen favourite; interviewers wanted Kubernetes-level depth
12. [OpenAI Playground](openai/openai_playground.md) — phone screen; front-end heavy

Then the rest of Tier 1, then Tier 2.

### All questions by tier

**Reports** counts the separate [PracHub][ph] entries merged into each
question, plus prep guides that name it. These are user-submitted and
unverified, so treat the counts as a popularity signal, not ground truth.

#### Tier 1 — must prepare

| Question | Reports | Most recent |
| --- | --- | --- |
| [Payment System (Holds, Capture, Batch Settlement)](openai/payment_system.md) | PracHub ×17 · Hello Interview staff top-5 · Coditioning · Interview Query | 2026-09-28 |
| [Cloud IDE / Devbox Service](openai/cloud_ide_devbox.md) | PracHub ×14 | 2026-10-12 |
| [Text-to-Video Generation Service (Sora-style)](openai/text_to_video_generation.md) | PracHub ×10 | 2026-09-28 |
| [Online Chess](openai/online_chess.md) | PracHub ×9 · Hello Interview staff #1 · Coditioning | 2026-09-21 |
| [ChatGPT](openai/chatgpt.md) | PracHub ×8 · Hello Interview staff top-5 · Educative | 2026-09-20 |
| [Device Monitoring over an Unreliable Network](openai/device_monitoring_unreliable_network.md) | PracHub ×8 | 2026-09-28 |
| [Slack (Team Messaging)](openai/slack.md) | PracHub ×6 · Hello Interview staff top-5 · Aced · Coditioning | 2026-04-26 |
| [Distributed Crossword Solver](openai/distributed_crossword_solver.md) | PracHub ×6 | 2026-05-12 |
| [CI/CD System (GitHub Actions)](openai/ci_cd_github_actions.md) | PracHub ×5 · Hello Interview staff top-5 · Coditioning · Interview Query | 2026-05-26 |
| [OpenAI Playground](openai/openai_playground.md) | PracHub ×3 · Aced (phone screen) | 2026-04-25 |
| [Webhook Delivery Platform](openai/webhook_delivery_platform.md) | Hello Interview · Coditioning · IGotAnOffer · PracHub ×1 | 2025-07-04 |
| [LLM-Powered Enterprise Search (RAG)](openai/enterprise_search_rag.md) | IGotAnOffer · DesignGurus | — |

#### Tier 2 — good to prepare

| Question | Reports | Most recent |
| --- | --- | --- |
| [Photo Storage with Content Deduplication](openai/photo_storage_dedup.md) | PracHub ×4 | 2026-09-20 |
| [In-Memory Key-Value Database](openai/in_memory_database.md) | PracHub ×4 | 2025-08-04 |
| [Usage Credits and Quotas](openai/credits_and_quotas.md) | PracHub ×3 · IGotAnOffer (GPU credits) | 2026-05-03 |
| [Real-Time Multiplayer Game (Trivia Battle Royale)](openai/realtime_multiplayer_game.md) | PracHub ×2 | 2026-10-10 |
| [Digital Game Store and Distribution (Steam)](openai/game_distribution_platform.md) | PracHub ×2 | 2026-09-18 |
| [URL Shortener](openai/url_shortener.md) | PracHub ×2 | 2026-01-19 |
| [Distributed Job Scheduler](openai/job_scheduler.md) | Aced (phone screen, ×2 accounts) | — |
| [Video Streaming Platform (Netflix)](openai/video_streaming_platform.md) | Aced (onsite) · Coditioning | — |
| [Distributed Rate Limiter](openai/rate_limiter.md) | PracHub ×1 · Interview Query | 2026-05-11 |
| [Metrics Monitoring and Alerting](openai/metrics_monitoring.md) | PracHub ×1 · Interview Query | 2026-10-01 |

#### Tier 3 — if you have time

| Question | Reports | Most recent |
| --- | --- | --- |
| [Real-Time Collaborative Editing](openai/collaborative_editing.md) | PracHub ×1 · IGotAnOffer | 2026-03-11 |
| [News Feed (Instagram)](openai/news_feed.md) | PracHub ×1 | 2026-05-25 |
| [Online Ads Serving](openai/ads_serving.md) | PracHub ×1 | 2025-09-06 |
| [Multi-Device Calendar](openai/calendar_app.md) | PracHub ×1 | 2025-11-09 |
| [Preventing Duplicate Request Processing](openai/idempotency_layer.md) | PracHub ×1 | 2026-04-04 |

### Left out on purpose

- *Regional surge pricing* and *search autocomplete* — tagged Machine Learning
  Engineer, not SWE.
- *Android MVVM API architecture* — mobile-specific.
- *"Design a fullstack app with frontend focus"* — no concrete system in the
  report.
- *Yelp, Foursquare, Twitter, notifications* — named by interviewing.io as
  screen prompts without dates or counts; covered by URL Shortener, News Feed
  and Webhook Delivery patterns.

### Sources

- [PracHub — OpenAI system design questions][ph] (116 entries, all six pages read; the site has a seniority filter, but none of the visible entries carry a level tag)
- [Hello Interview — OpenAI L5 guide](https://www.hellointerview.com/guides/openai/l5) and [L4 guide](https://www.hellointerview.com/guides/openai/l4)
- [Aced — OpenAI system design interview](https://www.aced.io/blog/openai-system-design-interview) and [Applied Engineer, Backend experience (2026)](https://www.aced.io/experiences/openai-software-engineer-interview-20a84c)
- [Coditioning — system design questions](https://www.coditioning.com/blog/16/openai-system-design-interview-questions) and [project deep dive guide](https://www.coditioning.com/blog/25/openai-swe-project-deep-dive)
- [interviewing.io — OpenAI interview process](https://interviewing.io/openai-interview-questions)
- [IGotAnOffer — OpenAI system design interviews](https://igotanoffer.com/en/advice/openai-system-design-interview) (blocked automated reads; used via search summaries)
- [DesignGurus — what to expect in the OpenAI system design interview](https://www.designgurus.io/answers/detail/what-to-expect-in-the-openai-system-design-interview)
- [Interview Query — OpenAI software engineer guide](https://www.interviewquery.com/interview-guides/openai-software-engineer)
- [Educative — OpenAI system design interview questions](https://www.educative.io/courses/openai-system-design-interview-questions)
- [PracHub — July 2026 ChatGPT onsite report](https://prachub.com/interview-experiences/openai-software-engineer-interview-experience-chatgpt-system-design-vector-store-and-a-scheduler-debugging-round-rejected)
- Level mapping: [Blind — OpenAI L5 vs Meta E6](https://www.teamblind.com/post/is-openai-downlevel-worth-it-mfu2dotq), [Blind — OpenAI vs stay at Meta](https://www.teamblind.com/post/openai-vs-stay-at-meta-agfuhj0b)
- [OpenAI — official interview guide](https://openai.com/interview-guide/)

Not covered: Hello Interview's community database (login required, including
its staff filter), and no first-hand account of a staff-to-L4 downlevel
turned up.

[ph]: https://prachub.com/companies/openai/categories/system-design
