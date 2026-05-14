<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Command Grammar

## Inter-agent command DSL

Commands are issued by the Director to Workers (and by Workers back to the Director) using
the following grammar inside the Task object's `description` field or in the
`runtime/agent_handoffs/current_mission.md` log.

```
<command> ::= <verb> <target> [<flags>]
<verb>    ::= RUN | REVIEW | ESCALATE | ABORT | RESUME | REPORT | REQUEST_CLEARANCE
<target>  ::= <task_id> | <agent_role> | "mission"
<flags>   ::= ("--" <key> "=" <value>)*
```

### Examples

```
REQUEST_CLEARANCE mission --reason="ready for data ingestion phase"
RUN T001 --owner=lead_quant
REVIEW T001 --owner=critical_reviewer --strict=true
ESCALATE T002 --reason="possible look-ahead bias in lag alignment"
ABORT mission --reason="HITL override"
RESUME mission --hitl_decision=approve
REPORT mission --format=markdown --to=runtime/run_reports/
```

## State mutation rules

- Only the currently assigned Worker may mutate state fields owned by its Task.
- The `hitl_decision` field may only be written by the human operator (mediated by the Director).
- Shared fields (`total_cost_usd`, `errors`, `model_calls`) may be appended to by any agent.
- Mission `status` transitions are owned by the Director only.
