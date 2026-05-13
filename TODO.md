# TODO Tracker — YipitData Signal Validation

> Single source of truth for in-flight work on `YIPIT-SIGNAL-001`. **Director updates on
> dispatch and completion.** Per-Task Briefs live in [`todos/`](todos/).

## Open

- `#TODO:` [m1/lead_quant] **T001** Data ingestion + sanity EDA — load both CSVs from `data/`, assert SHA-256, print sanity summary, one overlay plot. (target: M1; depends on: HITL clearance) — see [`todos/T001-data-ingestion.md`](todos/T001-data-ingestion.md)
- `#TODO:` [m2/lead_quant] **T002** Seasonal Naive Baseline — built FIRST, OOS MAPE/RMSE, full-sample + pandemic-excluded, cached to `runtime/benchmarks/baseline.json`. (target: M2; depends on: T001) — [`todos/T002-baseline-construction.md`](todos/T002-baseline-construction.md)
- `#TODO:` [m3/lead_quant] **T003** Walmart-fiscal aggregation + publication-lag-aware FRED merge with `merge_asof` and decision-date assertion. (target: M3; depends on: T002) — [`todos/T003-fred-merge-with-publication-lag.md`](todos/T003-fred-merge-with-publication-lag.md)
- `#TODO:` [m4/lead_quant] **T004** Forward-rolling OOS CV: M1 (OLS on FRED YoY) and optionally M2 (FRED + SN as second regressor) vs. baseline; bootstrap 95% CI on `delta_MAPE`. (target: M4; depends on: T003) — [`todos/T004-out-of-sample-cv.md`](todos/T004-out-of-sample-cv.md)
- `#TODO:` [m5/lead_quant] **T005** 2020 regime treatment + causal "why" + falsifiable headline claim. (target: M5; depends on: T004) — [`todos/T005-structural-break-analysis.md`](todos/T005-structural-break-analysis.md)
- `#TODO:` [m6/lead_quant+director] **T006** `memo.md` (≤ 1 page) + `prompts.md` (chronological log + < 200-word reflection) + final notebook polish. (target: M6; depends on: T005) — [`todos/T006-memo-and-prompts-log.md`](todos/T006-memo-and-prompts-log.md)
- `#TODO:` [continuous/critical_reviewer] **T999** Apply the standing audit checklist on every Review Request. — [`todos/T999-reviewer-audit-checklist.md`](todos/T999-reviewer-audit-checklist.md)

## Awaiting HITL

- `#TODO:` [hitl] **Clearance to dispatch T001.** Director acknowledgment is in `runtime/agent_handoffs/current_mission.md`. Append `HITL_DECISION: approve` (or `modify` with notes) to that file to release the gate.

## In Progress

*(empty — mission is in `PENDING_HITL_CLEARANCE`; nothing dispatched yet)*

## Done

- `#DONE:` [m0/director] **M0 — Bootstrap & Scaffolding** Kernel-aligned scaffolding mirroring `wojciechkrukar/agentic-workforce-kernel`: `.agent/` system prompts for the 3 personas (GPT-4o / Claude 3.5 Sonnet / OpenAI o1), `docs/kernel/` (vendored, generic), `docs/team/` (project extensions), `docs/projects/yipitdata-signal/` (challenge brief, methodology, data contracts, KPIs, caveats), `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md`, `todos/` (T001–T006 + T999), root `TODO.md` + `WALKTHROUGH.md` + YipitData-aware `README.md`, source CSVs copied verbatim into `data/`, stub deliverables (`analysis.ipynb`, `memo.md`, `prompts.md`) marked **BLOCKED — awaiting HITL clearance**, `runtime/agent_handoffs/current_mission.md` opened with `STATUS: PENDING_HITL_CLEARANCE`. (current PR)

## Discrepancies surfaced from `challange_docs/`

(per the user's instruction to flag any inconsistencies between the three challenge-doc formats)

- The three formats — `take_home_exam_candidate.md`, `take_home_exam_candidate.docx`,
  `take_home_exam_candidate.pdf` — are **content-identical**. The two `.docx` files have
  identical SHA-256 hashes (one is a duplicate copy). Only formatting differs across formats.
  See [`docs/projects/yipitdata-signal/caveats-and-discrepancies.md`](docs/projects/yipitdata-signal/caveats-and-discrepancies.md).
- The lockfile `challange_docs/~$ke_home_exam_candidate.docx` is a Word session-lock artefact,
  not challenge content. Optional follow-up: extend `.gitignore`.

## Open caveats / decisions for HITL to confirm

(restated from `docs/projects/yipitdata-signal/caveats-and-discrepancies.md` § "Open caveats")

- YoY-growth framing for the headline (vs. levels). Defaulting to YoY.
- Walmart fiscal-quarter alignment for FRED aggregation (vs. calendar quarter). Defaulting to fiscal.
- Pandemic disruption window definition: `2020Q1–2021Q1` (5 quarters). Defaulting to this.
- Conservative publication-lag assumption: `release_date = reference_period_end + 45 days` for both Walmart 10-Qs and FRED RSXFS releases.
- SN-A (`Q(t-4)`) as the default Seasonal Naive formulation; SN-B (with average growth) as a robustness check.

A `HITL_DECISION` of `approve` is taken to mean approval of these defaults. To override, append
`HITL_DECISION: modify` plus the override list, and the Director will rebrief T001 accordingly.
