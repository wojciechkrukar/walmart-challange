<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Task Contracts

A **Task** is the atomic unit of work assigned to a Worker agent.

## Schema

```json
{
  "task_id": "string (UUID or short slug)",
  "mission_id": "string",
  "title": "string",
  "description": "string",
  "assigned_to": "agent_role",
  "status": "PENDING | IN_PROGRESS | BLOCKED | REVIEW | DONE | FAILED | ESCALATED",
  "priority": 1,
  "inputs": {},
  "outputs": {},
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "deadline": "ISO-8601 | null",
  "depends_on": ["task_id", "..."]
}
```

## Lifecycle rules

- Only the Director may create or delete Tasks.
- A Worker sets status `IN_PROGRESS` when it picks up a Task.
- A Worker sets status `REVIEW` when it completes work and requests Critic review.
- A Critic sets status `DONE` (approved) or `FAILED` (rejected with `rejection_reason`).
- Three consecutive `FAILED` transitions trigger automatic escalation to `ESCALATED`.

## Output contract

Every Task output MUST include:
- `result` — the primary artifact path or inline payload.
- `confidence` — float 0–1.
- `cost_usd` — float, total LLM spend for the Task.
- `latency_ms` — int, wall-clock ms.
- `model_used` — string identifying the underlying model (or "human" for HITL outputs).
- `audit_notes` — a free-text section summarising what was checked and what was deferred.
