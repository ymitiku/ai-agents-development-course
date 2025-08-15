# Week 1 — Task List (Foundations: MCP + ADK)

**Dates:** Aug 18–24, 2025 (Africa/Addis_Ababa)  
**Due:** Sun, Aug 24, 2025, 23:00  
**Weight:** 15% total → Lab A 7%, Lab B 8%, Quiz 3%

---

## Lab A — MCP Tool Server Hardening (7%)

### A1. Schema & Contract Tightening
- [ ] Ensure `additionalProperties:false` across all I/O schemas.
- [ ] Add input validation rules (min/max, formats) and document them.
- [ ] Version schemas (e.g., `v1`) and note the change policy in `README` or `docs/`.
- [ ] Document **error taxonomy** (transient vs terminal) with codes/messages.

**Acceptance:** invalid inputs return structured 4xx (or MCP error) with clear messages; schemas pass validation.

### A2. Idempotency & Concurrency
- [ ] Confirm idempotency for `create_event` at **process** level (derive or accept an idempotency key).
- [ ] Document how collisions are handled; add a lock or safe section if needed.

**Acceptance:** Same `(title, when)` always returns identical `id` under concurrent calls (describe your strategy).

### A3. Health & Observability
- [ ] Add a health/readiness endpoint or equivalent MCP self-check.
- [ ] Emit **structured logs** with fields: tool name, args hash, attempt#, duration, error class.
- [ ] Capture at least one **retry** path in logs.

**Acceptance:** One run shows structured logs for success and for a retry case; health endpoint returns “ok”.

### A4. Docs
- [ ] Update `README.md` with: endpoints/commands, error taxonomy, schema versions, idempotency design.
- [ ] Add a short **ADR** (architecture decision record) for your schema/versioning and idempotency choices.

**Deliverables to submit (Lab A)**
- Repo link + commit hash  
- Screenshot or snippet of structured logs (success + retry)  
- One paragraph ADR summary (≤120 words)

---

## Lab B — ADK Agent: Robust Tool Use (8%)

### B1. Deterministic, Typed Outputs
- [ ] Ensure agent returns stable, typed fields (no extra keys; deterministic names).
- [ ] Propagate a `trace_id` (or equivalent) through tool calls into the final output.

**Acceptance:** Example call shows deterministic JSON with a `trace_id` echoed in agent output.

### B2. Reliability Controls
- [ ] Add **timeouts** per tool call.
- [ ] Add **retries** with exponential backoff + full jitter for transient failures.
- [ ] Implement a **step cap** and a **halting rule** (no unbounded loops).

**Acceptance:** One trace/log snippet demonstrates a retry attempt that then succeeds; max steps enforced.

### B3. ADK Web Demo Evidence
- [ ] Run `adk web` and invoke the agent calling `add` and `create_event`.
- [ ] Capture the **event log** (function call with args), and the **tool result** snippet.

**Acceptance:** Provide a screenshot/snippet showing `functionCall:add` (or `create_event`) and a result object.

### B4. Evaluation Run (Week 1 suite)
- [ ] Run a 50-case success test and record **success rate**, **p50**, **p95** latencies for agent→tool calls.
- [ ] Ensure ≥95% success; record p95 (no strict target this week; just report).

**Deliverables to submit (Lab B)**
- Repo link + commit hash  
- One ADK Web event log snippet (function call + result)  
- One trace/log snippet showing retry+success  
- 50-case summary line (success, p50, p95)

---

## Quiz 1 — Short Answer (3%)

Answer succinctly (2–4 sentences unless otherwise noted).

1) Define **idempotency** for tool calls and list one concrete strategy to implement it.  
2) Why prefer **typed outputs** over free-form text in tool-orchestrating agents?  
3) Name **two failure modes** good JSON Schemas help prevent.  
4) In ADK, what’s the purpose of a **run loop** and a **step cap**?  
5) Write a minimal **JSON input schema** (inline, ≤10 lines) for a `lookup_user(email)` tool.  
6) Which backoff strategy best reduces thundering herd: linear, fixed delay, or **exponential with jitter**—and why?  
7) Why should tool names and argument names be **stable and versioned**?  
8) What’s the difference between a **transient** error and a **terminal** error? Give one example of each.

**Deliverables to submit (Quiz 1)**
- Paste answers numbered **Q1–Q8** in chat.

---

## Submission Checklist (all Week 1)
- [ ] Repo link + commit hash (latest for Week 1)  
- [ ] Lab A artifacts: logs (success + retry), ADR paragraph  
- [ ] Lab B artifacts: ADK event snippet, retry trace, 50-case summary line  
- [ ] Quiz answers (Q1–Q8)

---

## Grading Rubric (Week 1 = 15%)
- **Lab A (7 pts)**  
  - Correctness & Contracts (3): schemas, validation, error taxonomy  
  - Reliability & Idempotency (2): idempotent `create_event`, concurrency note  
  - Observability (1): structured logs + health check  
  - Documentation (1): README/ADR updates
- **Lab B (8 pts)**  
  - Functionality (3): tool discovery & calls; typed/deterministic output with trace propagation  
  - Robustness (2): timeouts, retries with jitter, halting/step cap  
  - Evidence (2): ADK event log + retry trace  
  - Performance Reporting (1): 50-case success & latency line
- **Quiz 1 (3 pts)**  
  - Each question ≈0.375 pt; concise, accurate answers

---

## Suggested Work Plan (Mon–Sun)
- **Mon–Tue:** Lab A (schemas, errors, idempotency, health/logs)  
- **Wed–Thu:** Lab B (typed outputs, retries/timeouts, halting; ADK Web evidence)  
- **Fri:** 50-case evaluation run + logs  
- **Weekend:** Quiz 1 + polish docs; submit everything
