# Delivery KPIs — per-milestone exit criteria

> Each row in `docs/milestones.md` is "Done" only when ALL boxes below are checked.

## KPI priority reminder (from `docs/projects/walmart-signal-validation/kpis.md`)

1. Guardrail compliance (must be 0 violations)
2. OOS MAPE — Pre-COVID
3. OOS MAPE — Ex-COVID
4. OOS MAPE — Full sample
5. OOS RMSE
6. Reproducibility

---

## M0 — Bootstrap

- [x] `data/retail_sales_fred.csv` and `data/walmart_revenue.csv` present and unmodified.
- [x] `requirements.txt` lists pinned versions for pandas, numpy, statsmodels, matplotlib, jupyter.
- [x] `docs/kernel/**` vendored with provenance headers.
- [x] `docs/team/**`, `docs/projects/walmart-signal-validation/**`, `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md` scaffolded.
- [x] `runtime/{agent_handoffs,benchmarks,logs,run_reports,validation}/` directories present.

## M1 — Data Ingestion

- [x] FRED CSV loaded with `parse_dates`; monthly index verified.
- [x] Walmart CSV loaded with `parse_dates`; quarterly index verified; fiscal-quarter-end dates verified.
- [x] `fred_quarterly` aligned to Walmart fiscal Q ends.
- [x] `fred_yoy_lag1` and `walmart_yoy_lag1` constructed; lag verified by Critical Reviewer probe.
- [x] No external network library imported.

## M2 — Seasonal Naive Baseline

- [x] `Q(t) = Q(t-4) × (1 + μ)` implemented.
- [x] μ computed on the **training window only** in the rolling-CV harness — verified by Critical Reviewer probe.
- [x] Forward-rolling baseline MAPE / RMSE computed for Full / Pre-COVID / Ex-COVID.
- [x] Metrics persisted to `runtime/benchmarks/baseline.json`.

## M3 — Signal Model

- [x] OLS via `statsmodels.api` with `add_constant`.
- [x] Features = lag-1 only.
- [x] `summary()` printed in the notebook; in-sample R² explicitly labelled "annotation only".
- [x] No causal claim in the cell narrative.

## M4 — Out-of-Sample Rolling CV

- [x] Identical harness as the baseline (one CV loop, two predictors per fold).
- [x] No `KFold`, `ShuffleSplit`, or `train_test_split(..., shuffle=True)`.
- [x] Min training window ≥ 16 quarters.
- [x] MAPE + RMSE for Full, Pre-COVID, COVID, Post-COVID, Ex-COVID windows.

## M5 — COVID Structural-Break Audit

- [x] COVID window = 2020-Q1 .. 2021-Q1, named explicitly in the notebook.
- [x] `fig3_covid_break.png` rendered with shaded COVID window.
- [x] Sub-period MAPE table in the notebook AND in the memo.
- [x] Plain-English explanation of the channel-mix / stimulus driver.

## M6 — Executive Memo

- [x] One page (≤ 600 words).
- [x] Headline matches the verdict pattern in `docs/projects/walmart-signal-validation/kpis.md`.
- [x] Zero causal verbs ("causes", "drives", "leads to").
- [x] References the COVID structural-break section.
- [x] Discloses caveats: limited history, single ticker, no holdout reserved beyond the rolling CV, look-ahead protected by lag-1 only (not by quarterly-report publication date — see memo caveat).

## M7 — HITL Final Approval (open)

- [ ] HITL has read `memo.md` and `analysis.ipynb`.
- [ ] HITL has written `human_decision = "approve"` to the shared state (or its prose equivalent in this Mission's GitHub flow).
- [ ] Director has produced the final `runtime/run_reports/2026-05-13-walmart-signal-validation.md`.
