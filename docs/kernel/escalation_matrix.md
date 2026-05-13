<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Escalation Matrix

## Trigger conditions

| Condition | Action | Owner |
|-----------|--------|-------|
| Task fails 3× | Escalate to HITL | Director |
| Worker confidence < 0.4 | Flag for human review | Worker |
| Cost > project-defined budget | Alert + pause | Director |
| Latency > project-defined SLA | Log warning, continue | Worker |
| Critic rejects Worker output 3× consecutively | Force HITL review | Critic |
| Guardrail violation detected | Immediate halt | Critic |
| Data leakage / look-ahead bias detected | Immediate halt | Critic |
| Structural break in input data outside training distribution | Force HITL review | Worker |
| New LLM provider / tier swap proposed | Block + human approval | Reviewer |

## Escalation channels

1. `runtime/agent_handoffs/current_mission.md` — Director updates with escalation note.
2. Synchronous `interrupt()` — pauses the workflow for human input at a defined checkpoint.
3. `runtime/run_reports/` — Mission-end report includes an escalation summary.

## De-escalation

The human operator resumes the workflow by setting `human_decision` in the shared state to
one of: `approve | reject | reclassify | abort`.
