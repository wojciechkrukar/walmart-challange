# Escalation Matrix — walmart-signal-validation

> Project-specific escalation rules. For universal rules, see `docs/kernel/escalation_matrix.md`.

## Director-owned decisions

These conditions trigger escalation to the Director; no human is required unless the Director cannot resolve.

| Condition | Trigger | Director action |
|-----------|---------|-----------------|
| Lead Quant Task fails 3× | Third FAILED transition | Re-decompose the Task into smaller steps; if still failing, escalate to HITL |
| Critical Reviewer rejects same artifact 3× | Counter in `current_mission.md` | Convene a one-shot adjudication: present both sides to HITL |
| Statsmodels API mismatch (e.g., `add_constant` edge case on 1-row DataFrame) | Notebook execution error | Direct Lead Quant to use parameter-direct prediction; add a comment |
| Walmart fiscal calendar mis-mapping | FRED months land in the wrong fiscal quarter | Reference `docs/projects/walmart-signal-validation/architecture.md` §Fiscal-quarter mapping |
| Baseline outperforms model on full sample | Expected — see Mission Brief | Do NOT escalate — frame in memo as "conditional verdict" with COVID caveat |
| Pre-COVID model improvement < 10% | Marginal signal | Document in memo caveats; do not over-claim |

## Human-required decisions

These conditions cannot be resolved by agents alone; the Director MUST pause and request HITL input.

| Condition | Trigger | Action |
|-----------|---------|--------|
| External API call requested | Any non-CSV data ingestion proposed | **Immediate halt.** Mission Brief explicitly forbids APIs. Human must acknowledge before the Director will dispatch any further Tasks. |
| In-sample R² as headline metric | Critical Reviewer flags it after 3rd Quant rejection | Human reviews and confirms removal |
| Causal claim without controls | Memo claims FRED *causes* Walmart revenue | Human reviews the wording and either approves or rewrites |
| COVID handling | Any proposal to "fit through 2020" | Human must explicitly authorise — default is to honour the structural-break guardrail |
| `docs/kernel/**` modified | PR touches vendored kernel docs | Human must approve provenance bump (Class E PR) |
| Data file modified | Any `git diff` on `data/*.csv` | **Immediate halt.** Source data is read-only. |
| Different LLM tier proposed for any agent | PR modifies `docs/llm-roster.md` | Class E review — human approval required |

## Escalation channels

1. `runtime/agent_handoffs/current_mission.md` — Director updates status and blockers.
2. `prompts.md` orchestration log — every escalation is appended in chronological order.
3. `runtime/run_reports/YYYY-MM-DD-walmart-signal-validation.md` — final Mission summary lists all escalation events.
4. PR comment — Director leaves a blocking comment on any PR that violates a guardrail.

## De-escalation

The HITL operator resumes the Mission by writing one of the following decisions to the shared state and notifying the Director:

- `approve` — proceed as proposed
- `reject` — return to the Lead Quant with rationale
- `reclassify` — Mission scope change; new Mission Brief required
- `abort` — terminate Mission; produce abort report
