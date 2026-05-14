# Director Protocol — YipitData Signal Validation

> Project-specific extension of `docs/kernel/director_protocol.md`. Read the kernel doc first.

## Startup checklist

When beginning any Director session, execute in order:

1. **Read** `runtime/agent_handoffs/current_mission.md` — confirm `STATUS:` and any open `HITL_DECISION:` blocks.
2. **Read** `TODO.md` at repo root — identify Open items and their target milestones.
3. **Confirm** the mission is past `PENDING_HITL_CLEARANCE` before dispatching any Worker Task.
4. **Verify** `data/retail_sales_fred.csv` and `data/walmart_revenue.csv` exist and match the
   SHA-256 hashes recorded in `docs/projects/yipitdata-signal/data-contracts.md`.
5. **Verify** no Task is left in `IN_PROGRESS` from a previous session without a status note.

## Dispatch loop

```
WHILE mission status == IN_PROGRESS:
  FOR each open Task in TODO.md (sorted by target milestone, then priority):
    IF Task is BLOCKED → surface blocker; either resolve or escalate
    IF Task is PENDING and depends_on is satisfied:
        IF Task.assigned_to == "lead_quant"      → dispatch Task Brief to Lead Quant
        IF Task.assigned_to == "critical_reviewer" → dispatch Review Request to Reviewer
    AFTER each dispatch → append entry to runtime/agent_handoffs/current_mission.md
END
```

## YipitData-specific guardrail enforcement

The Director MUST refuse Worker outputs that violate any of these rules. These are restated
from the mission directive and from `docs/projects/yipitdata-signal/methodology.md`:

| Guardrail | Director action on violation |
|-----------|------------------------------|
| API call detected (FRED / yfinance / SEC EDGAR) | Reject; route back to Lead Quant |
| Output references files outside `data/` for primary inputs | Reject |
| Seasonal Naive Baseline absent or built **after** an alternative model | Reject |
| Lag alignment uses Walmart revenue with a release date later than the FRED snapshot | Reject |
| Any randomised K-fold or shuffled split appears in CV code | Reject |
| In-sample R² used as the success metric | Reject |
| 2020 fit through the structural break with no regime indicator or explicit caveat | Reject |
| Memo or notebook lacks an explicit "what would change my mind" statement | Reject |

## Merge / submission recommendation criteria

The Director may issue a "ready for human submission" recommendation only when **all** are true:
1. `analysis.ipynb` runs end-to-end from a fresh kernel without errors (Reviewer-attested).
2. `memo.md` exists, ≤ one printed page, and answers the four-part customer question.
3. `prompts.md` exists with a chronological prompt log and a < 200-word reflection note.
4. The Critical Reviewer has issued APPROVE on every checked-in artifact.
5. The anti-pattern audit checklist (`docs/kernel/review_policy.md`) is 100% addressed.
6. HITL has issued an explicit `HITL_DECISION: approve` in `current_mission.md`.

## Run report format

At mission end, produce `runtime/run_reports/YYYY-MM-DD-yipitdata-signal.md` with:
- Mission ID and objective
- Tasks dispatched, completed, failed, escalated
- Headline finding (signal beats baseline yes/no, by how much, on which OOS metric)
- Total LLM cost (USD) and wall-clock time
- Open items / known caveats carried forward
