## Task Brief

**Task ID:** T002
**Mission ID:** YIPIT-SIGNAL-001
**Title:** Seasonal Naive Baseline (built FIRST)
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** 1 (critical)
**Target milestone:** M2
**Depends on:** T001
**Status:** PENDING

### Objective

In `analysis.ipynb` § 2, implement the Seasonal Naive Baseline as a pure function over the
Walmart quarterly revenue series **only**. Run a forward-rolling out-of-sample evaluation of
the baseline. Cache the per-quarter and aggregate OOS errors to `runtime/benchmarks/baseline.json`.

This is the bar that any FRED-based model must clear. **The baseline is built before any
alternative model touches the data.** This ordering is non-negotiable per the mission directive.

### Inputs

- `data/walmart_revenue.csv` (do not touch FRED in this Task)
- `docs/projects/yipitdata-signal/methodology.md` § 4 (baseline formulation)
- `docs/projects/yipitdata-signal/kpis.md` (metric definitions, headline-cuts rule)

### Acceptance criteria

- [ ] Baseline implemented as a pure function with a docstring stating the formula.
- [ ] Both formulations are present (SN-A as default, SN-B as documented robustness check).
- [ ] OOS evaluation uses `TimeSeriesSplit` (or equivalent forward-rolling), initial train ≥ 16 quarters.
- [ ] Headline OOS MAPE and RMSE are reported full-sample AND pandemic-excluded.
- [ ] `runtime/benchmarks/baseline.json` is written with: full-sample MAPE/RMSE, pandemic-excluded MAPE/RMSE, and a per-quarter error table.
- [ ] No FRED columns appear in the baseline cell scope.
- [ ] No randomised CV anywhere; explicit comment confirms `shuffle=False`.

### Out of scope

- The FRED merge (T003).
- The FRED-augmented model (T004).
- Bootstrap confidence intervals on the baseline-alone numbers (deferred to T004 where the
  delta-vs-FRED CI is the headline).

### Forbidden

- Touching `data/retail_sales_fred.csv` in this Task.
- Reporting any in-sample fit statistic.
- Using `pd.DataFrame.sample()` or any other shuffle.

### Reviewer audit focus

- The baseline's prediction for quarter `t` uses **only** information available at the
  decision date for `t` (typically: `Q(t-4)` plus average growth from quarters strictly before
  the decision date).
- The OOS split is forward-rolling, not random; a print or assert confirms the split structure.
- The pandemic-excluded cut drops predictions whose target quarter falls in 2020Q1–2021Q1.
- The cached JSON schema matches what T004 will consume.
