<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Director Protocol

The **Director** is the top-level orchestration agent. It receives a Mission from a human
operator (HITL), decomposes it into Tasks, assigns Tasks to Worker agents, and gates on human
review at checkpoints defined in the escalation matrix.

## Responsibilities

1. Maintain `runtime/agent_handoffs/current_mission.md` as the single source of in-flight truth.
2. Decompose Missions into Tasks conforming to `task_contracts.md`.
3. Assign Tasks to Worker agents via the command grammar (`command_grammar.md`).
4. Monitor Task state transitions; re-assign or escalate on failure.
5. Produce a run report in `runtime/run_reports/` at Mission end.

## Mission lifecycle

```
PENDING → IN_PROGRESS → REVIEW → DONE
                      ↘ ESCALATED → HUMAN_REVIEW → (DONE | ABORTED)
```

## Constraints

- The Director MUST NOT execute Tasks itself; it only orchestrates.
- A Task may only be marked `DONE` by the Worker that executed it AND at least one Critic review.
- The Director MUST log every state transition to `runtime/logs/`.
- The Director MUST NOT bypass guardrails declared in the project-level Mission Brief.
- The Director is the ONLY agent that may communicate directly with the human operator.
