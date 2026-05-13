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

- [ ] HITL appends `HITL_DECISION: approve` (or `modify`) in `current_mission.md`.
- [ ] `analysis.ipynb` § 1 loads both CSVs from `data/` only.
- [ ] SHA-256 hashes asserted (not just printed) at the top of the notebook.
- [ ] Schema sanity prints: row counts, date ranges, NaN counts.
- [ ] One quick visual (overlay of YoY series) — clean, not polished.
- [ ] Reviewer's anti-pattern audit checklist filed in `runtime/validation/T001-review.md`.

## M2 — Seasonal Naive Baseline (T002)

- [ ] Baseline implemented as a pure function over the Walmart series only.
- [ ] OOS MAPE and RMSE for the baseline reported on a forward-rolling split.
- [ ] No predictor from FRED is touched in the baseline cell.
- [ ] Baseline numbers cached in `runtime/benchmarks/baseline.json`.
- [ ] Reviewer confirms: no leakage, no shuffled split, no in-sample R².

## M3 — FRED Lag-Aligned Merge (T003)

- [ ] FRED months aggregated to Walmart fiscal quarters (Feb–Apr = fQ1, etc.).
- [ ] Publication-lag rule from `methodology.md` applied; per-quarter decision date documented.
- [ ] Merged frame stored in-memory; not written back to `data/`.
- [ ] Reviewer signs off on the lag table; documents the assumed FRED release calendar.

## M4 — OOS Cross-Validation (T004)

- [ ] Forward-rolling CV implemented (no `KFold`, no `ShuffleSplit`).
- [ ] Initial training window ≥ 16 quarters.
- [ ] Headline `delta = MAPE_baseline − MAPE_FRED` reported with bootstrap 95% CI.
- [ ] Same headline reported on the pandemic-excluded cut.
- [ ] Per-quarter error table written to `runtime/benchmarks/oos_errors.json`.

## M5 — Structural-Break Analysis (T005)

- [ ] Pandemic window defined and shaded on the YoY plot.
- [ ] Either (a) regime dummy in the regression OR (b) sub-sample fit excluding the regime — reported.
- [ ] Memo includes a falsifiable headline claim per `kpis.md`.
- [ ] Causal "why" addressed (1–2 paragraphs).

## M6 — Submission Bundle (T006)

- [ ] `analysis.ipynb` runs end-to-end from a fresh kernel without errors.
- [ ] `memo.md` ≤ 1 printed page; answers all four parts of the customer question.
- [ ] `prompts.md` chronological log + < 200-word reflection.
- [ ] Critical Reviewer issues APPROVE on the bundle (Class E).
- [ ] HITL appends final `HITL_DECISION: approve`.
- [ ] Director writes `runtime/run_reports/<date>-yipitdata-signal.md`.
