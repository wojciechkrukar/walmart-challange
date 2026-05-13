# Escalation Matrix — YipitData Signal Validation

> Project-specific escalation rules. For universal rules, see `docs/kernel/escalation_matrix.md`.

## Director-resolvable escalations

These conditions trigger escalation to the Director; no human is required unless the Director cannot resolve.

| Condition | Trigger | Director action |
|-----------|---------|-----------------|
| Lead Quant Task fails 3× | Three FAILED transitions | Decompose the Task; reassign with a tighter Task Brief |
| Reviewer cannot verify a numerical result | Reviewer issues REQUEST_CHANGES with "non-reproducible" finding | Ask Lead Quant to add an inline assertion that re-derives the number |
| Notebook breaks Restart-and-Run-All after a code-cell mutation | CI / dry-run check fails | Block the artifact; route back to Lead Quant |
| Reviewer and Lead Quant disagree on what counts as "look-ahead" for a given lag | Two REQUEST_CHANGES rounds with no convergence | Director picks the more conservative alignment; documents the choice in `methodology.md` |

## HITL-required escalations

These conditions cannot be resolved by agents alone; the Director MUST pause and request human operator input.

| Condition | Trigger | Action |
|-----------|---------|--------|
| Mission stuck in `PENDING_HITL_CLEARANCE` after Director acknowledgment | Awaiting initial green light | Director re-pings HITL with the Task Brief preview; does **not** dispatch |
| Conflict between the literal text of the customer brief and the mission directive's guardrails | Lead Quant or Reviewer flags inconsistency | Surface to HITL with a side-by-side diff |
| Suspected data-quality issue in the source CSVs (gaps, duplicates, fiscal-year boundary issues) | SHA hash matches but content looks wrong | HITL must confirm the CSVs are the canonical inputs before any rework |
| Memo headline finding flips between two Reviewer rounds | "Signal beats baseline" → "does not beat" or vice versa | HITL reviews both versions before final lock-in |
| Time cap (4–6 h human time-equivalent) is at risk of being exceeded | Director's wall-clock estimate vs. completed Tasks | HITL decides whether to scope-down or extend |

## Escalation channels

1. `runtime/agent_handoffs/current_mission.md` — Director appends an `ESCALATION:` block.
2. `runtime/run_reports/` — mission-end report includes every escalation event.
3. PR comment — when running through GitHub, the Director leaves a blocking PR comment.

## De-escalation

The HITL operator resumes the mission by appending a `HITL_DECISION:` block to
`current_mission.md` containing:
- Decision verb: `approve` | `reject` | `modify`
- Rationale (1–3 sentences)
- Next allowed Task IDs (or `all-open` to clear the gate)
