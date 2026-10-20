# OpenAI Technical Deep Dive (Project Presentation)

A reverse system design round. You present a project you led; the
interviewer stress-tests it. Along with the design rounds, it weighs most in
whether you land at L5 or L4.

Video: [ShowOffer — Crack the Project Retro / Technical Deep Dive Interview at OpenAI & Anthropic](https://www.youtube.com/watch?v=Y_D114Tr5nI)

## Format (as reported)

- 45–60 minutes with an engineer or senior manager, sometimes a silent shadow,
  sometimes from another team.
- About 15–20 minutes presenting, 25–40 minutes of questions. One account had
  a 30-minute talk and 15 minutes of Q&A — confirm with your recruiter.
- Slides expected even if not requested. Read like engineering docs, not a
  pitch. Bring 2–3 backup slides: one candidate prepared two problems, was
  asked for more, and needed the backups.
- If your loop had a take-home, ask whether the deep dive covers that or a
  career project.

## Choosing the project

- One **you defined and led** — your decisions, not a famous system where you
  owned a corner.
- **Scale matters.** A candidate presenting a startup project with nine
  enterprise customers was told it lacked the scale OpenAI wanted. If scale
  is small, say so first and explain what changes at 10× and 100×.
- Every technology on your slides is an invitation to an internals probe
  (Kafka rebalancing, Kubernetes scheduling, WAL recovery, cross-shard
  transactions). Keep only what you can explain.

## Slide outline

1. **Context** (1–2 slides): the problem, why it mattered, scale — users,
   QPS, data volume, money or latency at stake.
2. **My role:** what I owned and decided, who else did what. Say "I" for your
   decisions and "we" only for team work.
3. **Architecture:** diagram and data flow.
4. **Key decisions** (the core): for each, the options, why this one, what it
   cost. Two or three decisions, not ten.
5. **What went wrong:** at least one incident, failed bet or performance
   cliff — diagnosis, fix, prevention.
6. **Results:** measured outcomes — latency, error rate, throughput, cost,
   adoption by other teams. Not "shipped on time".
7. **Limits and hindsight:** where it breaks next, and the concrete technical
   change you'd make now plus why you didn't make it then.

## Staff signals to make visible

- You set the technical direction, not just executed it.
- Influence across team boundaries: how you got other teams to adopt,
  change, or agree, and how you handled disagreement.
- You chose what *not* to build.
- Operational ownership: SLOs, on-call pain, the incident you led.
- Multi-quarter arc: v1 → v2 and why the evolution happened.

## Questions to rehearse

- Walk me through it end to end. What exactly did you own?
- What was the hardest trade-off? What did you give up?
- Why this database / queue / framework? How does it work internally?
- What failed in production, and how did you respond?
- How did you measure success?
- What are the scaling limits? What breaks first at 10×?
- Who disagreed with you, and how was it resolved?
- What would you do differently, concretely?
- What else was hard? (Have a second and third problem ready.)

## Failure modes

- "We" everywhere — the interviewer can't find your decisions.
- Buzzword stack that collapses under one internals question.
- Only successes.
- Hindsight like "better communication" instead of a technical change.
- Ten minutes of background, so the decisions section gets cut.

## Prep checklist

- [ ] Project chosen; scale numbers written on the context slide
- [ ] Re-read the design docs, incident reports and key PRs
- [ ] Every named technology: can explain internals for 3 minutes
- [ ] Two backup problems with a slide each
- [ ] Timed run-through at 15–20 minutes, then a mock Q&A with someone
      hostile
- [ ] Confidentiality checked; recruiter told early if anything is sensitive
