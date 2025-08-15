# AI Agent Development — Personalized Syllabus (v1)

**Learner profile (confirmed):**
- **Occupation:** Machine Learning Engineer
- **Expertise:** Python, ML/DL, NLP, Computer Vision, LLMs
- **Education:** B.Sc. Software Engineering; M.Sc. Machine Intelligence
- **Languages:** English, Amharic
- **Agentic AI exposure:** ADK “hello world,” simple agents, one workflow agent
- **Preferred learning style:** pragmatic + deep dive

**Course length:** 6 weeks • **Effort:** 5–7 hrs/week • **Style:** hands-on, project-first, **pragmatic + deep-dive**, optional **bilingual glossaries (EN ↔ አማ)** • **Timezone:** Africa/Addis_Ababa (UTC+3)

---

## Outcomes
By the end you will be able to:
1. Explain and implement the core agent loop (observe → think → act) with tool-calling & structured outputs.
2. Build production-minded RAG, memory, and planning components.
3. Orchestrate multi-agent systems (e.g., planner+worker, supervisor+specialists) using a modern framework (ADK / LangGraph / Assistants / crewAI) and vanilla Python when needed.
4. Evaluate agents with task-specific metrics (success rate, tool latency, cost, safety violations) and create red-team checks.
5. Deploy to a cloud target with secrets, logging, and monitoring.

---

## Personalization for You
- **Rigor bump:** keep Week 2 accuracy goal at **≥85%** (vs. 80%) and p95 latency target **<1.8s** to match your experience.
- **Deep-dive tracks:** prefer protocol internals (MCP/AAP), memory architectures, and Agentic RAG planning heuristics.
- **Language support:** I can append short **Amharic summaries** at the end of each week and maintain a bilingual glossary on request.
- **Recommended capstones (pick one):**
  1) **Research Copilot (Agentic RAG)** focused on ML papers/Kaggle EDA.
  2) **Document Understanding Agent** (e.g., prescriptions/invoices) with QA reviewer over AAP.
  3) **Workflow Coach** that proposes/executes small experiments and logs results.

---

## Tooling & Setup (Week 0)
- **Runtime:** Python 3.11–3.12, `uv` or Poetry for envs, Docker for packaging.
- **Frameworks & Orchestration (pick primary, compare others):**
  - **Google Agent Development Kit (ADK)** as the primary orchestrator
  - LangGraph, crewAI, Assistants API for comparisons
- **Protocols & Interop:**
  - **Model Context Protocol (MCP)** for tool servers & capability discovery
  - **Google's Agent-to-Agent protocol (AAP)** for inter-agent communication
- **Retrieval:** FAISS or pgvector; optional reranker
- **Observability:** OpenTelemetry + structured logs; optional LangSmith-equivalent
- **Local models (optional):** Ollama + small instruct model for fast iterations
- **Quality-of-life:** pre-commit, ruff/black, pytest

**Deliverable:** Environment repo with `make dev`, `make test`, `make run`, **one MCP tool server** (e.g., calculator + calendar), and an **ADK agent** that calls those MCP tools and returns a deterministic JSON schema.

---

## Weekly Plan (6 weeks)

### Week 1 — Foundations: Agents, Tools, and MCP
- Agent loop, function/tool calling, schema design, error handling, retries/timeouts
- **MCP basics:** tool servers, capability negotiation, schema validation
- **ADK basics:** tool adapters, state, and run loops
- **Lab A:** Build a minimal **MCP tool server** exposing `add(a,b)` and `create_event(title, when)`
- **Lab B:** Build an **ADK agent client** that discovers and calls the MCP tools; add timeouts/retries and typed outputs
- **Checkpoints:**
  - MCP schema validation passes for 50 calls; deterministic JSON
  - ADK agent ≥95% success on 50-case function-call test

### Week 2 — Retrieval-Augmented Generation (RAG) — Baseline
- Indexing pipelines, chunking & metadata, query rewriting, re-ranking; citations & confidence
- **Lab:** Build a **RAG answerer in ADK** with a vector store (FAISS/pgvector) and citation rendering; expose retrieval as an MCP tool so other agents can reuse it
- **Checkpoints:**
  - Answer accuracy ≥80% on a handcrafted eval set
  - Latency p95 < 2s on warm cache

### Week 3 — Agentic RAG, Planning & Memory
- Planner vs. scratchpad; **Agentic RAG** (iterative querying, tool switching, verification)
- Episodic vs. semantic memory; storing and reusing partial results
- **Lab:** Implement a **planner agent** in ADK that:
  1) reformulates queries; 2) calls the RAG MCP tool; 3) verifies/critics; 4) writes salient facts to memory; 5) produces a final, cited answer
- **Checkpoints:**
  - Compositional question accuracy improves ≥10% vs. Week 2 baseline
  - Second-turn performance improves with memory read/write

### Week 4 — Multi-Agent Patterns & Google AAP
- Supervisor/worker, router/specialist, debate/critique loops; halting & backoff
- **AAP basics:** message envelopes, roles, routing rules; safety considerations
- **Lab:** Build a **two-agent system over AAP**: a Data-Extractor specialist + a QA-Reviewer that negotiates corrections via AAP; include deadlock detection & max-steps safeguards
- **Checkpoints:**
  - End-to-end precision/recall vs. single-agent baseline improves ≥10%
  - AAP message validation passes; no unbounded loops

### Week 5 — Evaluation, Observability, and Safety
- Golden tasks, synthetic evals, adversarial prompts, regression tests; telemetry & tracing; cost/time budgets
- **Lab:** Build an eval harness (CLI) that runs suites, logs traces, and outputs a gate (pass/fail) for CI; include **tool-use metrics** and **AAP/MCP protocol conformance**
- **Checkpoints:**
  - Non-regression suite (≥100 cases) with pass rate threshold
  - Trace viewer screenshot + p95 latency chart

### Week 6 — Deployment & Capstone
- Containerization, config/secrets, horizontal scaling, model fallbacks; minimal UI
- **Capstone must include:**
  - One **MCP tool server**
  - An **ADK-orchestrated** agent (single- or multi-agent)
  - **RAG** (baseline) + at least one **Agentic RAG** behavior
  - **AAP** if multi-agent
- **Deliverables:** Live endpoint or CLI, README, demo video (≤3 min), eval results, and architecture diagram

---

## Assessment Rubric (per milestone)
- **Functionality (35%)**: task success/correctness on evals
- **Reliability (20%)**: retries, timeouts, idempotency, deterministic schemas
- **Observability (15%)**: logs/traces, metrics, error taxonomy
- **Design (15%)**: clear abstractions, testability, separation of concerns
- **Security/Safety (10%)**: secrets handling, guardrails, PII hygiene
- **Protocol Conformance (5%)**: MCP schema validation, AAP message compliance

**Pass bar:** ≥80% overall and no red flags (secrets in repo, missing timeouts, protocol violations)

---

## Habit Loop & Support
- **Cadence:** 2 build sessions + 1 evaluation session weekly
- **Reflection:** 5-minute retro per week (what worked, what failed, one improvement)
- **Check-ins:** End-of-week checkpoint summary + next-week goals (template below)

**Checkpoint template**
- What I built:
- Eval summary (accuracy, p95 latency, cost):
- Biggest failure + root cause:
- Next week’s focus:

---

## Stretch Tracks (pick any)
- **ADK Deep Dive:** tool adapters, state stores, agents-as-services, queue workers
- **AAP in Production:** routing strategies, topic partitions, failure recovery, telemetry
- **Advanced RAG:** hybrid search, query planning, feedback signals, grounded generation
- **Safety:** jailbreak taxonomy, content filters, self-checks, model calling policies

---

## What I’ll Provide
- Fast feedback on labs and capstone scope
- Targeted code review (structure, evals, reliability, **protocols**)
- Extra drills if any concept feels shaky
- **Professor/Tutor mode:** I will grade each submission against the rubric, track your cumulative score, and provide narrative feedback + remediation tasks.

---

## Course Operations (Professor/Tutor Mode)
**How we’ll work**
- **Submissions:** Post repo link + required logs directly in this chat. I will grade and update your gradebook here in the doc.
- **Allowed Tools:** You may use AI coding assistants and libraries, but **note them in the README** and keep runs reproducible.
- **Submission format:**
  - Code: GitHub link + commit hash and `README.md` with run commands
  - Logs: paste CLI output blocks requested by each assignment
  - Short answers/quizzes: number your answers clearly (e.g., Q1–Q8)
- **Academic integrity:** Cite external resources and prompts; keep evaluation data separate from training data.
- **Feedback loop:** I’ll return a score + brief comments + a targeted improvement task for the next week.

**Grading Weights (100%)**
- Week 0 Diagnostic — **5%**
- Week 1 (MCP/ADK Foundations): **15%** (Lab A 7%, Lab B 8%)
- Week 2 (RAG Baseline): **15%** (Lab 12%, Quiz 3%)
- Week 3 (Agentic RAG): **20%** (Lab 15%, Quiz 5%)
- Week 4 (Multi-Agent w/ AAP): **15%** (Lab 12%, Peer Review 3%)
- Week 5 (Eval/Obs/Safety): **10%** (Lab 10%)
- Week 6 (Capstone): **20%** (Build 16%, Demo 4%)

**Letter grades**: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, F < 60
