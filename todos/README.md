# Task Briefs — YipitData Signal Validation

> One Markdown file per Task ID. Files are created and owned by the Director. Workers consume
> them via the assignment pointed to in `TODO.md`.

| Task ID | Title | Owner | Reviewer | Target Milestone | Depends on |
|---|---|---|---|---|---|
| [T001](T001-data-ingestion.md)                       | Data ingestion + sanity EDA                          | lead_quant | critical_reviewer | M1 | clearance |
| [T002](T002-baseline-construction.md)                | Seasonal Naive Baseline (built FIRST)                | lead_quant | critical_reviewer | M2 | T001 |
| [T003](T003-fred-merge-with-publication-lag.md)      | Walmart-fiscal aggregation + lag-aligned FRED merge  | lead_quant | critical_reviewer | M3 | T002 |
| [T004](T004-out-of-sample-cv.md)                     | Forward-rolling OOS CV: FRED signal vs. baseline     | lead_quant | critical_reviewer | M4 | T003 |
| [T005](T005-structural-break-analysis.md)            | 2020 regime treatment + causal "why"                 | lead_quant | critical_reviewer | M5 | T004 |
| [T006](T006-memo-and-prompts-log.md)                 | `memo.md` + `prompts.md` finalisation                | lead_quant + director | critical_reviewer + director | M6 | T005 |
| [T999](T999-reviewer-audit-checklist.md)             | Standing audit checklist for the Critical Reviewer   | critical_reviewer | n/a (self-applied) | continuous | none |

These Task Briefs are templates **not yet dispatched**. The mission is in
`PENDING_HITL_CLEARANCE` (see `runtime/agent_handoffs/current_mission.md`); the Director will
dispatch T001 only after the human appends `HITL_DECISION: approve`.
