# System Design

## OpenAI question bank

26 distinct questions, deduplicated from about 116 candidate-reported OpenAI
system design prompts plus the questions named in prep guides (compiled
2026-10-19). Every question uses the same answer skeleton —
**[TEMPLATE.md](TEMPLATE.md)** explains the template and how to grade yourself.

**How to practise one:** set a 60-minute timer, fill in the question file
top to bottom, then open its **Interviewer notes** and score yourself with the
rubric in the template. Log the attempt at the bottom of the file and redo
weak ones a week later.

**Reports** counts the separate [PracHub][ph] entries merged into each
question, plus prep guides that name it. These are user-submitted and
unverified, so treat the counts as a popularity signal, not ground truth.

### Tier 1 — must prepare

| Question | Reports | Most recent |
| --- | --- | --- |
| [Payment System (Holds, Capture, Batch Settlement)](openai/payment_system.md) | PracHub ×17 · Hello Interview top-5 · Coditioning · Interview Query | 2026-09-28 |
| [Cloud IDE / Devbox Service](openai/cloud_ide_devbox.md) | PracHub ×14 | 2026-10-12 |
| [Text-to-Video Generation Service (Sora-style)](openai/text_to_video_generation.md) | PracHub ×10 | 2026-09-28 |
| [Online Chess](openai/online_chess.md) | PracHub ×9 · Hello Interview #1 · Coditioning | 2026-09-21 |
| [ChatGPT](openai/chatgpt.md) | PracHub ×8 · Hello Interview top-5 · Educative | 2026-09-20 |
| [Device Monitoring over an Unreliable Network](openai/device_monitoring_unreliable_network.md) | PracHub ×8 | 2026-09-28 |
| [Slack (Team Messaging)](openai/slack.md) | PracHub ×6 · Aced · Hello Interview · Coditioning | 2026-04-26 |
| [Distributed Crossword Solver](openai/distributed_crossword_solver.md) | PracHub ×6 | 2026-05-12 |
| [CI/CD System (GitHub Actions)](openai/ci_cd_github_actions.md) | PracHub ×5 · Hello Interview top-5 · Coditioning · Interview Query | 2026-05-26 |
| [OpenAI Playground](openai/openai_playground.md) | PracHub ×3 · Aced (phone screen) | 2026-04-25 |
| [Webhook Delivery Platform](openai/webhook_delivery_platform.md) | Hello Interview · Coditioning · IGotAnOffer · PracHub ×1 | 2025-07-04 |

### Tier 2 — good to prepare

| Question | Reports | Most recent |
| --- | --- | --- |
| [Photo Storage with Content Deduplication](openai/photo_storage_dedup.md) | PracHub ×4 | 2026-09-20 |
| [In-Memory Key-Value Database](openai/in_memory_database.md) | PracHub ×4 | 2025-08-04 |
| [Usage Credits and Quotas](openai/credits_and_quotas.md) | PracHub ×3 | 2026-05-03 |
| [Real-Time Multiplayer Game (Trivia Battle Royale)](openai/realtime_multiplayer_game.md) | PracHub ×2 | 2026-10-10 |
| [Digital Game Store and Distribution (Steam)](openai/game_distribution_platform.md) | PracHub ×2 | 2026-09-18 |
| [URL Shortener](openai/url_shortener.md) | PracHub ×2 | 2026-01-19 |
| [Distributed Job Scheduler](openai/job_scheduler.md) | Aced (phone screen) | — |
| [Video Streaming Platform (Netflix)](openai/video_streaming_platform.md) | Aced (onsite) · Coditioning | — |
| [Distributed Rate Limiter](openai/rate_limiter.md) | PracHub ×1 · Interview Query | 2026-05-11 |
| [Metrics Monitoring and Alerting](openai/metrics_monitoring.md) | PracHub ×1 · Interview Query | 2026-10-01 |

### Tier 3 — if you have time

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

### Sources

- [PracHub — OpenAI system design questions][ph] (116 entries, all six pages read)
- [Hello Interview — OpenAI L5 guide](https://www.hellointerview.com/guides/openai/l5) and [L4 guide](https://www.hellointerview.com/guides/openai/l4)
- [Aced (formerly Exponent) — OpenAI system design interview](https://www.aced.io/blog/openai-system-design-interview)
- [Coditioning — OpenAI system design interview questions](https://www.coditioning.com/blog/16/openai-system-design-interview-questions)
- [IGotAnOffer — OpenAI system design interviews](https://igotanoffer.com/en/advice/openai-system-design-interview) (page blocked automated reads; used via search summary)
- [Interview Query — OpenAI software engineer guide](https://www.interviewquery.com/interview-guides/openai-software-engineer)
- [Educative — OpenAI system design interview questions](https://www.educative.io/courses/openai-system-design-interview-questions)
- [PracHub — July 2026 ChatGPT onsite report](https://prachub.com/interview-experiences/openai-software-engineer-interview-experience-chatgpt-system-design-vector-store-and-a-scheduler-debugging-round-rejected)

Not covered: Hello Interview's community question database needs a login, and
Glassdoor and Blind weren't searched directly.

[ph]: https://prachub.com/companies/openai/categories/system-design
