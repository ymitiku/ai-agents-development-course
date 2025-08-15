# Week 0 — Detailed Syllabus (Diagnostic & Setup)

**Dates:** Aug 15–17, 2025 (Africa/Addis_Ababa)  
**Due:** **Sun, Aug 17, 2025, 23:00**  
**Weight:** **5%** of final grade

---

## 1) Learning Objectives
By the end of Week 0 you will:
- Stand up a clean, reproducible development environment (Python + package manager + Docker).
- Implement a minimal **MCP tool server** with validated JSON Schemas and structured errors.
- Build a minimal **ADK agent** that discovers and calls the MCP tools with typed outputs.
- Containerize the system and expose a CLI for smoke tests.

---

## 2) Required Deliverables
1) **Repo Scaffold (production-minded)**
   - `README.md` with clear setup/run/test instructions.
   - `Makefile` (or `justfile`) with at least: `dev`, `run`, `test`, `lint`, `format`, `eval`, `build`, `docker-run`.
   - Packaging with **Poetry** or **uv**, pinned lockfile committed.
   - Pre-commit hooks (black/ruff) configured.

2) **MCP Tool Server** (HTTP or stdio; your choice)
   - Tools:
     - `add(a:int, b:int) -> {"total": int, "trace_id": str}`
     - `create_event(title:str, when:datetime) -> {"id": str, "when_iso": str}`
   - JSON Schemas for inputs/outputs (`additionalProperties: false`).
   - Error taxonomy: **transient** vs **terminal**; consistent error payloads.
   - Idempotency for `create_event` (e.g., deterministic key from inputs or explicit idempotency key).

3) **ADK Agent (client)**
   - Discovers the MCP server, validates schemas.
   - Calls both tools with **timeouts**, **retries** (exponential + jitter), and **typed outputs** (Pydantic/TypedDict).
   - Step cap + halting rule (no unbounded loops).

4) **Containerization**
   - Multi-stage Dockerfile (builder → runtime).
   - `make build` and `make docker-run` work on a clean machine.

5) **Smoke Tests & Logs**
   - 50 randomized `add` calls → report success rate (target ≥ **95%**).
   - 10 malformed `create_event` calls → show 4xx error bodies and messages.
   - One trace/log of a call that **retries** at least once.

---

## 3) Acceptance Criteria (pass/fail for Week 0 credit)
- MCP schemas validate; bad inputs rejected with helpful messages.
- ADK agent achieves **≥95%** success on 50 `add` calls.
- Deterministic, typed JSON outputs (stable field names).
- Container builds and runs; CLI commands function as documented.

---

## 4) Submission Instructions (paste in chat)
- **Repo link + commit hash**
- **CLI output** line showing the 50-case summary (success/failed + p95 latency)
- **One retry trace/log** (redacted if needed)
- **1–2 sentences** on the trickiest issue and how you fixed it

---

## 5) Suggested Schedule
- **Day 1:** Repo scaffold, environment, pre-commit, project layout
- **Day 2:** Implement MCP server + schemas + error taxonomy; local smoke tests
- **Day 3:** ADK agent (discovery + calls + retries/timeouts + typed outputs), Dockerize, run smoke tests, finalize README

---

## 6) Project Layout (suggested)
```

ai-agents/
├─ agents/
│  ├─ adk\_agent/              # minimal ADK client
│  └─ **init**.py
├─ tools/
│  └─ mcp\_server/             # MCP tool server (HTTP or stdio)
│     ├─ schemas/             # JSON Schemas (inputs/outputs)
│     └─ **init**.py
├─ shared/
│  ├─ logging.py              # structured logs + trace helpers
│  └─ types.py                # Pydantic models / TypedDicts
├─ tests/
│  ├─ test\_add.py
│  └─ test\_create\_event.py
├─ scripts/
│  ├─ run\_smoke.py            # 50-case harness
│  └─ run\_malformed.py        # 10 malformed cases
├─ Dockerfile
├─ pyproject.toml             # or uv project files
├─ README.md
└─ Makefile

````

---

## 7) Makefile Targets (example)
```make
.PHONY: dev run test lint format build docker-run eval

dev:        ## create venv, install deps, install pre-commit
	uv venv || true
	uv pip install -r requirements.txt || true
	pre-commit install

run:        ## run MCP server locally
	python -m tools.mcp_server.app

test:       ## run unit tests
	pytest -q

lint:
	ruff check .

format:
	ruff format .

eval:       ## smoke tests (50 add, 10 malformed)
	python scripts/run_smoke.py && python scripts/run_malformed.py

build:
	docker build -t ai-agents:week0 .

docker-run:
	docker run --rm -p 8000:8000 ai-agents:week0
````

---

## 8) JSON Schemas (starter)

**`add`**

```json
{
  "name": "add",
  "input_schema": {
    "type": "object",
    "properties": { "a": { "type": "integer" }, "b": { "type": "integer" } },
    "required": ["a", "b"],
    "additionalProperties": false
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "total": { "type": "integer" },
      "trace_id": { "type": "string" }
    },
    "required": ["total", "trace_id"],
    "additionalProperties": false
  }
}
```

**`create_event`**

```json
{
  "name": "create_event",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "minLength": 1 },
      "when":  { "type": "string", "format": "date-time" }
    },
    "required": ["title", "when"],
    "additionalProperties": false
  },
  "output_schema": {
    "type": "object",
    "properties": {
      "id": { "type": "string" },
      "when_iso": { "type": "string", "format": "date-time" }
    },
    "required": ["id", "when_iso"],
    "additionalProperties": false
  }
}
```

---

## 9) Retry/Timeout Pattern (example)

```python
import random, time

def backoff_sleep(attempt: int):
    time.sleep(min(0.5 * (2 ** attempt) + random.random() / 10, 8.0))

def call_with_retries(fn, *, max_attempts=5, timeout_s=8.0):
    for attempt in range(max_attempts):
        try:
            return fn(timeout=timeout_s)
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            backoff_sleep(attempt)
```

---

## 10) Dockerfile (multi-stage skeleton)

```dockerfile
# --- builder ---
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml ./
# If using Poetry: install and build wheels
RUN pip install --no-cache-dir poetry && poetry export -f requirements.txt -o requirements.txt --without-hashes
COPY . .
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

# --- runtime ---
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "-m", "tools.mcp_server.app"]
```

---

## 11) Test Harness (50-case smoke)

```python
# scripts/run_smoke.py
import random, uuid, time
from statistics import median

def call_add(a, b): ...
def measure():
    latencies = []
    ok = 0
    for _ in range(50):
        a, b = random.randint(-10**6,10**6), random.randint(-10**6,10**6)
        t0 = time.time()
        out = call_add(a,b)
        latencies.append(time.time()-t0)
        if out["total"] == a + b and "trace_id" in out:
            ok += 1
    p95 = sorted(latencies)[int(len(latencies)*0.95)-1]
    print(f"[W0] add: success={ok}/50, p50={median(latencies):.3f}s, p95={p95:.3f}s")

if __name__ == "__main__":
    measure()
```

---

## 12) Grading (Week 0 = 5%)

* **MCP server (2 pts):** schemas validate; structured errors; idempotency for `create_event`.
* **ADK agent (1 pt):** discovery + typed outputs + retries/timeouts.
* **Mini RAG (1 pt):** *not required in Week 0* (moved to Week 2).
  *(If you already add a `retrieve()` tool, you can earn 0.5 bonus.)*
* **Containerization (1 pt):** multi-stage build; runs via `make docker-run`.

> **Note:** The syllabus keeps Week 0 focused on environment + minimal agent/tool. RAG comes in Week 2.

---

## 13) Quality Bar (what I look for)

* Deterministic field names and types; no undocumented fields.
* Clean logs: tool name, args hash (no PII), attempt count, timings, error class.
* Clear separation of concerns (server vs agent vs shared types).
* Reproducible `make` targets; no hidden manual steps.

---

## 14) What to Do Next

1. Create the scaffold and MCP server.
2. Build the ADK client with retries/timeouts + typed outputs.
3. Containerize and run smoke tests.
4. Post your **repo + logs** in chat for grading.

