# Prep Binder: handoff for a new Claude chat

Paste this whole file into a new chat (or say "read HANDOFF.md from my repo") so Claude can continue exactly where we stopped.

## 1. Who we are and the goal
- Two friends preparing for backend interviews, about **3 years of experience** each.
- **Shreyash**: Python (learning FastAPI). **Friend**: Java (learning Spring Boot). Both in India; Hinglish is fine for WhatsApp messages.
- Both are **first-time learners of Kafka** and use these notes as their **only** Kafka source, so Kafka notes must be complete and in depth.
- We study on weekdays, post updates in a WhatsApp group, and keep weekends light.

## 2. Daily structure (weekdays, ~2 hrs 15 min)
| Block | Time |
|---|---|
| Recall warm-up (previous day's topics + one older problem, no coding) | 10 min |
| DSA: Striver A2Z sheet, **2 problems a day, 1 on hard days** (watch Striver video, then solve) | 60 min |
| LLD topic (sudoCODE videos + extra topics) | 25 min |
| Kafka: **one topic per day, in depth** | 30 min |
| SQL: one concept + one LeetCode SQL 50 problem | 10 min |
| Mystery Pattern (Mon, Wed, Fri): one **medium array** LeetCode problem; we guess two pointers / hashing / sliding window ourselves. **Never reveal the pattern.** | 15 min |

- Friday: only 1 new DSA problem + **30 min weekly revision** (redo problems we couldn't recall, skim one-line insights, quiz on the week's LLD/Kafka/SQL).
- After every DSA problem we write a one-line insight.
- Weekends: Saturday backlog only if needed; **API concepts 45 min Sat + 45 min Sun**.

## 3. Where we are (as of Thu, Nov 26, 2026)
- **Week 3 (Nov 23–29)** is live on the site. Week 4 Mon–Tue (Nov 30, Dec 1) is also on the site; Week 4 Wed–Fri still to plan.
- **Kafka**: Days 1–8 done (PDFs on site). Next: Day 9 consumer groups and rebalancing (Thu Nov 26), Day 10 replication (Fri Nov 27).
- **SQL**: Days 1–8 done. Next: Day 9 UNION vs UNION ALL (practice LC 1789), Day 10 CASE WHEN and conditional aggregation (LC 1934).
- **DSA (A2Z arrays)**: Week 3 = Set Matrix Zeroes, Rotate Matrix, Spiral, Count Subarray Sum K, Pascal's Triangle, Majority II, 3 Sum, 4 Sum. Week 4 Mon: Largest Subarray 0 Sum, Subarrays XOR K; Tue: Merge Overlapping Intervals, Merge Sorted Arrays Without Extra Space. Continue with A2Z order after that (Repeating and Missing, Count Inversions, Reverse Pairs, Max Product Subarray, then Binary Search step).
- **LLD**: OOP and SOLID done. Week 3: DRY/KISS/YAGNI/Law of Demeter, Singleton, Factory Method, Abstract Factory, Builder. Week 4: Prototype (Mon), Adapter (Tue).
- **Pending, not urgent**: upgrade Kafka Days 1–5 (add self-check quizzes to Days 1–3; add retention configs + `kafka-consumer-groups --reset-offsets` command + mistakes + quiz to Day 4; add `compression.type`, `max.request.size`, `message.max.bytes` + mistakes + quiz to Day 5).

## 4. Roadmaps still ahead
**Kafka (finish by Dec 11, 30 min/day):** 9 Consumer groups & rebalancing · 10 Replication (leader/follower, ISR, controller picks new leader) · 11 Producer acks, retries, idempotent producer · 12 Delivery semantics · 13 Retention, log compaction, ZooKeeper vs KRaft (in detail: what ZooKeeper did, why removed, Raft controller quorum, metadata log, migration) · 14 Hands-on: Kafka in Docker + CLI · 15 Hands-on: producer/consumer in Python and Java · 16 Retries, dead letter queues, poison messages · 17 Idempotent consumers and duplicates · 18 Performance and scaling (why Kafka is fast, partition count, consumer lag) · 19 Outbox pattern and CDC · 20 Kafka in system design + mock interview. (Dropped: Kafka Streams, Connect, Schema Registry in depth.)

**SQL (10 min/day, ~6 weeks total):** 11 Window functions I (ROW_NUMBER/RANK/DENSE_RANK, LC 178) · 12 Window functions II (LAG/LEAD, running totals, LC 180) · then CTEs, recursive CTEs, date/string functions, views, indexes (clustered vs non-clustered, composite, when they hurt), EXPLAIN, normalization 1NF–BCNF, transactions/ACID, isolation levels and anomalies, locking and deadlocks, optimistic vs pessimistic locking, SQL vs NoSQL, partitioning/sharding, hard patterns (Nth highest per group, consecutive records, top-N per group). Focus on **PostgreSQL**, note MySQL differences.

**LLD:** structural patterns (Decorator, Facade, Proxy, Composite, Bridge, Flyweight) → behavioral (Strategy, Observer, Command, State, Template Method, Chain of Responsibility, Iterator, Mediator, Memento, Visitor) → concurrency and thread safety → clean code and testing → machine coding (Parking Lot, LRU Cache, Elevator, Vending Machine, Splitwise, BookMyShow, Rate Limiter, Notification Service, Logger, Cache with TTL, Pub-Sub, Job Scheduler, LLM API Gateway).

**API concepts (weekends):** Weekend 2 (Nov 28–29) Sat API design (naming, versioning, pagination, filtering), Sun validation, error handling, DTOs, request flow in FastAPI/Spring Boot · Weekend 3 DB + ORM (entities, migrations, transactions, N+1, connection pooling) · Weekend 4 security (auth vs authz, sessions vs JWT, hashing, CORS, rate limiting, idempotency keys). After that: project.

**Project (after ~1 month of Kafka + API):** event-driven Order & Payment system: Order Service (Spring Boot, friend) + Payment Service (FastAPI, Shreyash) + Notification Service, PostgreSQL, Kafka, idempotent consumers, retries + DLQ, Outbox pattern, tests, Docker Compose, README with architecture diagram.

## 5. Notes format we like
- PDFs made with Python **ReportLab**, A4, navy/orange style, DejaVu fonts (see `tools/common.py`; examples `tools/kd8.py`, `tools/sql8.py`, `tools/week3.py`). No emoji inside PDFs.
- **Kafka notes (fuller format):** goal box → concept step by step with diagrams → under-the-hood details → **config settings table** → commands and **Python + Java code** → common mistakes table → interview questions labeled **Very common / Common / Good to know** with likely follow-ups → situation-based scenarios (problem → solution → trade-off) → **self-check quiz** → recap → next-day recall.
- **SQL notes:** visual diagrams of tables/results, PostgreSQL focus, edge cases, one LeetCode practice with a **hint, not the solution**, labeled interview questions, 1–2 scenarios, recap.
- Never repeat earlier content; build on previous days. Check diagrams for overlapping text before sharing.

## 6. How the website works
- Site: Vercel (static), repo **shreyashtiwari06/prep-binder**. Vercel redeploys automatically on every commit to `main`.
- `index.html` (plain HTML/CSS/JS, views: Home with daily motivation, Day by day with week strip, All notes) reads `data.json`. PDFs live in `pdfs/`.
- `data.json` item format:
```json
{ "track": "Kafka", "day": 9, "title": "Consumer groups and rebalancing", "date": "2026-11-26",
  "pdf": "pdfs/Kafka_Day9_Consumer_Groups.pdf", "points": ["optional bullet lines"],
  "links": [{ "label": "Striver: 3 Sum", "url": "https://youtu.be/..." }] }
```
  `track` is one of DSA, LLD, Kafka, SQL, Schedule. DSA/LLD items also have `"when": "Week 3, Mon Nov 23"`. Weekly plan PDFs use track `Schedule` with `day` = week number.
- Video links: we send direct YouTube links; until then use YouTube search links (`https://www.youtube.com/results?search_query=take+U+forward+striver+<problem>`). Claude can't open YouTube or takeuforward.org itself.
- To update the site, Claude uses `tools/push.py` with a GitHub token that **we paste at the start of the chat** (fine-grained token, only this repo, Contents: Read and write, 90 days). **Never store the token in the repo.**

## 7. How we like Claude to behave
- Warm, honest, concise. Say plainly when something isn't possible or isn't sure (e.g. can't verify a video link) instead of guessing.
- Ask **one** clear question when something is ambiguous (e.g. which day's notes we mean), and confirm before big changes to the plan.
- Keep plans realistic for people with full-time jobs; prefer adjusting over overloading.
- When we share updates, summarise what went well, the backlog, and one pattern to improve, without lecturing.
- Give WhatsApp-ready messages in code blocks when asked (English or Hinglish).
- For each new day: make the Kafka/SQL PDFs, upload them, and attach them to the right **date** in `data.json`.
