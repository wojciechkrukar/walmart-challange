# Telemetry — walmart-signal-validation

> What we capture per agent run. Telemetry is best-effort: missing telemetry is a warning, not a Mission halt.

## Per-Task telemetry

Every Task closes with the following entry appended to `runtime/logs/<YYYY-MM-DD>.jsonl`:

```json
{
  "ts": "2026-05-13T21:30:08Z",
  "mission_id": "WAL-2026-05-13",
  "task_id": "P2-baseline-construction",
  "agent": "Lead Quant",
  "model": "claude-opus-4.7",
  "tier": "tier1",
  "verb": "RUN",
  "duration_ms": 0,
  "cost_usd": 0.0,
  "outcome": "DONE",
  "critic_verdict": "APPROVED",
  "critic_score": 0.95,
  "guardrail_violations": []
}
```

For this in-context Mission (no live LLM calls), `cost_usd` and `duration_ms` are recorded as 0 and the `model` field is the *intended* model from `docs/llm-roster.md`.

## Per-Mission telemetry

At Mission close, the Director writes `runtime/run_reports/YYYY-MM-DD-walmart-signal-validation.md` summarising:

- Total Tasks dispatched / approved / rejected / escalated
- Critic-rejection breakdown by Phase
- KPI snapshot from `runtime/benchmarks/baseline.json`
- All escalation events
- All `guardrail_violations` ever raised (target: 0)

## What is NOT logged

- The contents of the data files (already in `data/`).
- Raw LLM prompts / responses (live runs would log these to LangSmith; not applicable here).
- Personal data — none is present in the Mission inputs.
