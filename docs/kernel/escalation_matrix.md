<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Escalation Matrix

## Trigger conditions

| Condition | Action | Owner |
|-----------|--------|-------|
| Task fails 3× consecutively | Escalate to HITL | Director |
| Worker confidence < 0.4 | Flag for Critic review | Worker |
| Critic rejects same Worker output 3× | Escalate to HITL | Director |
| Worker requests scope change | Pause Task; route to Director | Worker |
| Cross-domain dependency discovered mid-Task | Pause Task; route to Director | Worker |
| Mission still `PENDING_HITL_CLEARANCE` after dispatch attempt | Refuse dispatch; remind HITL | Director |
| Any guardrail in `docs/projects/<name>/` violated | Halt mission; escalate to HITL | Critic |

## Escalation channels

1. `runtime/agent_handoffs/current_mission.md` — updated with the escalation note and reason.
2. `runtime/run_reports/` — mission-end summary includes every escalation event.
3. PR comment — Director leaves a blocking comment on any PR carrying the offending change.

## De-escalation

The human operator resumes the mission by editing `current_mission.md`:
- Set `STATUS:` to the next valid lifecycle state.
- Append a `HITL_DECISION:` block with the rationale.
- The Director resumes the dispatch loop on the next cycle.
