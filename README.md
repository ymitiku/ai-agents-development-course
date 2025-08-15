# AI Agent Development — Course & Lab Repo
This repository hosts both the **course syllabus** and the **code** that will be built while progressing through a 6-week, hands-on curriculum focused on practical AI agent development.

> **Core stack:** Google **ADK** (primary orchestrator), **MCP** (Model Context Protocol) for tool servers, Google **AAP** (Agent-to-Agent Protocol) for inter-agent comms, **RAG** baseline, and **Agentic RAG** (planning + iterative retrieval).

---

## Table of Contents
- [Goals & Outcomes](#goals--outcomes)
- [Repository Layout](#repository-layout)
- [Getting Started](#getting-started)
- [Makefile / Common Tasks](#makefile--common-tasks)
- [Week 0 Diagnostic (Quickstart)](#week-0-diagnostic-quickstart)
- [How to Submit Work](#how-to-submit-work)
- [Grading & Progress Tracking](#grading--progress-tracking)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Goals & Outcomes
By the end of this course, the goal is to have a solid foundation in AI agent development, including:

1. Implement the **agent loop** (observe → think → act) with tool calling & typed outputs.  
2. Build production-minded **RAG**, memory, and planning components.  
3. Orchestrate **multi-agent** systems using ADK (plus comparisons to LangGraph/crewAI/Assistants).  
4. **Evaluate** agents with success, latency, cost, and safety metrics; run adversarial checks.  
5. **Deploy** to a cloud target with secrets, logging, tracing, and monitoring.

For the full syllabus (main topics only), see:  
[docs/syllabus/main.md](docs/syllabus/main.md)

---

## Repository Layout
Recommended structure (create as you go):

```

.
├─ docs/
│  └─ syllabus/
│     ├─ main.md                # The main 6-week overview (topics-only)
│     ├─ week0.md               # Detailed syllabus (Diagnostic & Setup)
│     ├─ week1.md               # Detailed syllabus (Foundations: MCP/ADK)
│     └─ weekN.md               # Additional weeks as separate docs
│
├─ agents/
│  └─ adk_agent/
│     ├─ **init**.py
│     └─ cli.py                 # e.g., `python -m agents.adk_agent.cli demo`
│
├─ tools/
│  └─ mcp_server/
│     ├─ **init**.py
│     ├─ app.py                 # MCP server (HTTP or stdio)
│     └─ schemas/
│        ├─ add.json
│        └─ create_event.json
│
├─ retrieval/
│  ├─ index.py                  # RAG indexing pipeline (Week 2)
│  └─ store/                    # FAISS/pgvector glue, metadata, reranker hooks
│
├─ evals/
│  ├─ suites/                   # golden tasks & regression sets
│  └─ harness.py                # CLI to run evals and output JSON summaries
│
├─ scripts/
│  ├─ run_smoke.py              # 50-case harness (Week 0)
│  └─ run_malformed.py          # malformed-input tests (Week 0)
│
├─ tests/
│  ├─ test_add.py
│  └─ test_create_event.py
│
├─ shared/
│  ├─ logging.py                # structured logs & trace helpers
│  └─ types.py                  # Pydantic models / TypedDicts
│
├─ Dockerfile
├─ pyproject.toml               # Poetry/uv project
├─ README.md
└─ Makefile

````

---

## Getting Started

### Prerequisites
- **Python** 3.11+ (3.12 recommended)
- **Docker** (for containerization and parity)
- **Poetry** for dependency management (or `uv` if preferred)
- (Optional) **Ollama** for local models

### Setup (Poetry)
```bash
poetry install
poetry run pre-commit install
poetry run python -m tools.mcp_server.app  # start MCP server locally
````


### Run the ADK Agent (example)

```bash
poetry run adk demo
```

### Containerize

```bash
make build
make docker-run
```

> Keep all commands reproducible via the **Makefile**. No hidden manual steps.

---

## Makefile / Common Tasks

```make
.PHONY: dev run test lint format build docker-run eval

dev:        ## create venv, install deps, install pre-commit
	poetry install || true
	poetry run pre-commit install || true

run:        ## run MCP server locally
	poetry run python -m tools.mcp_server.app

test:       ## run unit tests
	poetry run pytest -q

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

eval:       ## smoke tests (50 add, 10 malformed)
	poetry run python scripts/run_smoke.py && poetry run python scripts/run_malformed.py

build:
	docker build -t ai-agents:week0 .

docker-run:
	docker run --rm -p 8000:8000 ai-agents:week0
```

---

## Week 0 Diagnostic (Quickstart)

> **Detailed syllabus:** `docs/syllabus/week0.md`

**Deliverables**

1. **MCP tool server** exposing:

   * `add(a:int,b:int) -> {"total": int, "trace_id": str}`
   * `create_event(title:str, when:datetime) -> {"id": str, "when_iso": str}`
   * JSON Schemas with `additionalProperties:false`
   * Error taxonomy (transient vs. terminal) + idempotency for `create_event`
2. **ADK agent** that discovers MCP tools and calls them with:

   * timeouts, retries (exponential + jitter), typed outputs, step cap/halting
3. **Containerization** (multi-stage Dockerfile)
4. **Smoke tests & logs**

   * 50 randomized `add` calls → **≥95%** success
   * 10 malformed `create_event` calls → 4xx bodies visible
   * One trace/log showing a retry path

**Submit in Chat**

* Repo link + commit hash
* 50-case summary line (success/failed + p95)
* One retry trace/log
* 1–2 sentences on the trickiest issue and your fix

---

## How to Submit Work

For each week:

1. Push your code and docs.
2. Paste in chat:

   * Repo link + **commit hash**
   * The **required logs** (as specified in that week’s syllabus)
   * Answers to any **quizzes** (Q1–Qn)

ChatGPT will grade, give feedback, and update your running score.

---

## Grading & Progress Tracking

Weights (100% total):

| Component                      | Weight |
| ------------------------------ | :----: |
| Week 0 Diagnostic              |   5%   |
| Week 1 (MCP/ADK Foundations)   |   15%  |
| Week 2 (RAG Baseline)          |   15%  |
| Week 3 (Agentic RAG)           |   20%  |
| Week 4 (Multi-Agent w/ AAP)    |   15%  |
| Week 5 (Eval/Obs/Safety)       |   10%  |
| Week 6 (Capstone Build + Demo) |   20%  |

Letter grades: **A ≥ 90**, **B ≥ 80**, **C ≥ 70**, **D ≥ 60**, **F < 60**

**Live Gradebook** (update in `docs/syllabus/main.md` or a separate `GRADEBOOK.md`):

| Component          |   Weight | Status            | Score |
| ------------------ | -------: | ----------------- | ----: |
| Week 0 Diagnostic  |       5% | Not yet submitted |     — |
| Week 1 Lab A       |       7% | Not yet submitted |     — |
| Week 1 Lab B       |       8% | Not yet submitted |     — |
| Week 1 Quiz        |       3% | Not yet submitted |     — |
| Week 2 Lab         |      12% | —                 |     — |
| Week 2 Quiz        |       3% | —                 |     — |
| Week 3 Lab         |      15% | —                 |     — |
| Week 3 Quiz        |       5% | —                 |     — |
| Week 4 Lab         |      12% | —                 |     — |
| Week 4 Peer Review |       3% | —                 |     — |
| Week 5 Lab         |      10% | —                 |     — |
| Week 6 Capstone    |      16% | —                 |     — |
| Week 6 Demo        |       4% | —                 |     — |
| **Total**          | **100%** |                   |       |

---

## Roadmap

* **Week 1:** Foundations (MCP tool server + ADK client, typed outputs, retries/timeouts, halting)
* **Week 2:** **RAG** baseline (indexing, metadata, query rewriting, reranking, citations)
* **Week 3:** **Agentic RAG** (planner → retrieve → verify, memory)
* **Week 4:** **Multi-Agent** patterns + **AAP** (supervisor/worker; router/specialist)
* **Week 5:** **Evaluation/Observability/Safety** (golden tasks, adversarial, tracing)
* **Week 6:** **Deployment & Capstone** (containerization, secrets, monitoring, demo)

Stretch tracks:

* Deeper ADK internals; production AAP routing; advanced RAG (hybrid, rerankers); guardrails & self-checks.

---

## Troubleshooting

* **Schemas rejecting inputs?** Ensure `additionalProperties:false` and correct required fields/types.
* **Retries not triggering?** Differentiate **transient** vs **terminal** errors; only retry transient.
* **Unbounded loops?** Add a **step cap** and a **halting rule**.
* **Docker build fails?** Prefer a multi-stage Dockerfile; pin dependencies via lockfile.
* **Non-deterministic outputs?** Enforce typed responses (Pydantic/TypedDict) with stable field names.

---

## License

This repository is licensed under the **MIT License** unless otherwise noted. See `LICENSE` for details.

