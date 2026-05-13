# Director Protocol — walmart-signal-validation

> Project-specific extension of `docs/kernel/director_protocol.md`. Read the kernel doc first for universal rules; this file adds project-specific startup checks, dispatch details, and escalation thresholds.

## Startup checklist

When beginning any Director session for this Mission, execute in order:

1. **Read** `runtime/agent_handoffs/current_mission.md` — note current Mission ID, status, owner, blockers.
2. **Check** `TODO.md` at repo root — identify Open `#TODO:` items and their target milestones.
3. **Verify** the data files are present and readable:
   - `data/retail_sales_fred.csv`
   - `data/walmart_revenue.csv`
4. **Confirm** the guardrails from the Mission Brief are echoed in `docs/projects/walmart-signal-validation/kpis.md` and have not been silently relaxed.
5. **Check** `runtime/benchmarks/baseline.json` for the latest Seasonal Naive baseline metrics.
6. **Review** any open critique left by the Critical Reviewer in the most recent run report.

## Dispatch loop

```
FOR each open #TODO: in TODO.md (sorted by milestone priority):
  IF task is BLOCKED → surface blocker, attempt resolution or escalate
  IF task is PENDING and owner is identified → dispatch Task Brief to owner agent
  IF task has no owner → assign per `docs/team/collaboration.md` ownership table
  AFTER each Worker completion → dispatch REVIEW to Critical Reviewer
  AFTER Critical Reviewer approval → mark #DONE: with date and one-line summary
  AFTER each dispatch → update runtime/agent_handoffs/current_mission.md
END
```

## Project-specific escalation thresholds

| Condition | Threshold | Director action |
|-----------|-----------|-----------------|
| Look-ahead bias suspected | Any Critic flag | Halt Lead Quant; require lag-alignment proof in `architecture.md` before resuming |
| In-sample R² used as headline metric | Any occurrence in the notebook narrative | Reject; require Lead Quant to remove or relabel as illustrative |
| K-fold / shuffled CV introduced | Any `KFold`, `ShuffleSplit`, or random index permutation | Reject immediately; this is a hard guardrail |
| Baseline not built before signal model | Notebook section order violation | Reject; Phase 2 may not start until Phase 1 is `DONE` |
| COVID structural break smoothed over | Any line fit through 2020 without commentary | Require Lead Quant to add the structural-break section per `docs/projects/walmart-signal-validation/structural-breaks.md` |
| External API call introduced | Any `requests`, `urllib`, `pandas_datareader`, etc. | Reject; only `data/*.csv` reads permitted |
| Critical Reviewer rejects same artifact 3× | Counter in current_mission.md | Escalate to HITL with both Quant draft and Critic rationale |
| Memo claims causation without evidence | Any "causes" / "drives" without lag + control | Require Lead Quant to soften to "is associated with" and add caveat |

## Merge / delivery recommendation criteria

The Director may issue a "ready for HITL final approval" recommendation only when ALL of the following are true:

1. `analysis.ipynb` executes end-to-end without errors (`jupyter nbconvert --execute --inplace`).
2. The Critical Reviewer has signed off on every Phase-exit gate (M1–M6).
3. `runtime/benchmarks/baseline.json` matches the metrics quoted in the memo.
4. No `guardrail_violations` are present in the most recent state snapshot.
5. The memo addresses every numbered guardrail from the Mission Brief.
6. `docs/projects/walmart-signal-validation/structural-breaks.md` is referenced from both the notebook and the memo.

## Run report format

At Mission end, produce `runtime/run_reports/YYYY-MM-DD-walmart-signal-validation.md` with:
- Mission ID, objective, HITL principal
- Tasks dispatched, completed, failed, escalated
- Critical-Reviewer verdicts per Phase
- KPI snapshot from `runtime/benchmarks/baseline.json`
- Guardrails matrix with pass / fail per item
- Open items carried forward (none expected for this single-Mission project)
