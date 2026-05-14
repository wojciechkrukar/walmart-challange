# Delivery KPIs — YipitData Signal Validation

> Per-milestone exit criteria mapped to the strict KPI priority order in
> [`docs/projects/yipitdata-signal/kpis.md`](projects/yipitdata-signal/kpis.md).

## KPI priority reminder

1. Anti-pattern audit pass rate (100% required)
2. Notebook reproducibility (Restart-and-Run-All)
3. Honest answer to the customer question
4. OOS error of FRED-based model vs. baseline
5. Regime-aware reporting

---

## M0 — Bootstrap & Scaffolding

- [x] Kernel docs vendored, generic, read-only (provenance header on each file).
- [x] Three personas formally defined in `docs/team/roles.md` and `.agent/`.
- [x] LLM roster locked to the directive's profiles for Tier 1.
- [x] Source CSVs in `data/` with SHA-256 hashes recorded in `data-contracts.md`.
- [x] `current_mission.md` opens with `STATUS: PENDING_HITL_CLEARANCE`.
- [x] No analysis code committed yet (the directive requires HITL clearance first).

## M1 — HITL Clearance & Data Ingestion (T001)

- [x] HITL appends `HITL_DECISION: approve` (or `modify`) in `current_mission.md`.
- [x] `analysis.ipynb` § 1 loads both CSVs from `data/` only.
- [x] SHA-256 hashes asserted (not just printed) at the top of the notebook.
- [x] Schema sanity prints: row counts, date ranges, NaN counts.
- [x] One quick visual (overlay of YoY series) — clean, not polished.
- [x] Reviewer's anti-pattern audit checklist filed in `runtime/validation/T001-review.md`.

## M2 — Seasonal Naive Baseline (T002)

- [x] Baseline implemented as a pure function over the Walmart series only.
- [x] OOS MAPE and RMSE for the baseline reported on a forward-rolling split.
- [x] No predictor from FRED is touched in the baseline cell.
- [x] Baseline numbers cached in `runtime/benchmarks/baseline.json`.
- [x] Reviewer confirms: no leakage, no shuffled split, no in-sample R².

## M3 — FRED Lag-Aligned Merge (T003)

- [x] FRED months aggregated to Walmart fiscal quarters (Feb–Apr = fQ1, etc.).
- [x] Publication-lag rule from `methodology.md` applied; per-quarter decision date documented.
- [x] Merged frame stored in-memory; not written back to `data/`.
- [x] Reviewer signs off on the lag table; documents the assumed FRED release calendar.

## M4 — OOS Cross-Validation (T004)

- [x] Forward-rolling CV implemented (no `KFold`, no `ShuffleSplit`).
- [x] Initial training window ≥ 16 quarters.
- [x] Headline `delta = MAPE_baseline − MAPE_FRED` reported with bootstrap 95% CI.
- [x] Same headline reported on the pandemic-excluded cut.
- [x] Per-quarter error table written to `runtime/benchmarks/oos_errors.json`.

## M5 — Structural-Break Analysis (T005)

- [x] Pandemic window defined and shaded on the YoY plot.
- [x] Either (a) regime dummy in the regression OR (b) sub-sample fit excluding the regime — reported.
- [x] Memo includes a falsifiable headline claim per `kpis.md`.
- [x] Causal "why" addressed (1–2 paragraphs).

## M6 — Submission Bundle (T006)

- [x] `analysis.ipynb` runs end-to-end from a fresh kernel without errors.
- [x] `memo.md` ≤ 1 printed page; answers all four parts of the customer question.
- [x] `prompts.md` chronological log + < 200-word reflection.
- [x] Critical Reviewer issues APPROVE on the bundle (Class E).
- [x] HITL appends final `HITL_DECISION: approve`.
- [x] Director writes `runtime/run_reports/<date>-yipitdata-signal.md`.
