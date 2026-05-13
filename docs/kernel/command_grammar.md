<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Command Grammar

## Inter-agent command DSL

Commands are issued by the Director to Workers via the Task object's `description` field
using the following grammar:

```
<command> ::= <verb> <target> [<flags>]
<verb>    ::= RUN | REVIEW | ESCALATE | ABORT | RESUME | REPORT
<target>  ::= <node_name> | <task_id> | "mission"
<flags>   ::= ("--" <key> "=" <value>)*
```

### Examples

```
RUN ingestion --inputs=data/retail_sales_fred.csv,data/walmart_revenue.csv
REVIEW baseline --task_id=uuid --strict=true
ESCALATE rolling_cv --reason="lag_alignment_dispute"
ABORT mission --reason="guardrail_violation"
RESUME hitl_gate --human_decision=approve
REPORT mission --format=markdown
```

## State mutation rules

- Only the currently assigned Worker may mutate state fields in its declared domain.
- Shared fields (`total_cost_usd`, `errors`, `model_calls`) may be appended to by any node.
- The `guardrail_violations` field may only be written by a Critic.
- The `human_decision` field may only be written by the HITL Gate after human input.
- The `terminal_sink` field may only be written by the Router / Director at Mission close.
