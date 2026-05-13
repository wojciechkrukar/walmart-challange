# Phase 1 Plan — Data Ingestion + Seasonal Naive Baseline

> Owner: Lead Quant. Critic: Critical Reviewer. Director gate: required before Phase 2.

## Objective

Load the two CSV inputs, align them to Walmart's fiscal calendar, construct the lag-1 features, and build the formal Seasonal Naive Baseline. Freeze the baseline metrics into `runtime/benchmarks/baseline.json`.

## Inputs

- `data/retail_sales_fred.csv` — monthly U.S. retail sales (FRED RSXFS), USD millions.
- `data/walmart_revenue.csv` — Walmart quarterly revenue (USD millions), fiscal-quarter-end dated.

## Steps

| Step | Notebook section | Acceptance |
|------|------------------|-----------|
| 1.1 | `## 1. Load data` | Both DataFrames loaded with `parse_dates`; assert no NaN in revenue / sales; print head + dtype |
| 1.2 | `## 2. Aggregate FRED to fiscal quarters` | FRED monthly → quarterly, aligned to Walmart's fiscal-Q ends (Apr/Jul/Oct/Jan); record the mapping in `architecture.md` |
| 1.3 | `## 3. Construct lag-1 features` | `fred_yoy_lag1`, `walmart_yoy_lag1` constructed only from data ≤ Q(t-1); the cell is the chokepoint flagged in `kpis.md` G3 |
| 1.4 | `## 4. Seasonal Naive Baseline` | Q(t) = Q(t-4) × (1 + μ), where μ is the *training-window* mean YoY; assertion that μ is recomputed per fold in the rolling CV |
| 1.5 | `## 5. Baseline OOS metrics` | Forward-rolling MAPE / RMSE for full, pre-COVID, ex-COVID windows; persisted to `runtime/benchmarks/baseline.json` |

## Exit criteria (Phase Gate 1 — Critical Reviewer)

- [ ] Both DataFrames pass dtype + range assertions
- [ ] Fiscal-quarter mapping table matches `architecture.md`
- [ ] Lag-1 features verified: for any fold ending at index i, `train.iloc[:i]` does not contain `test.iloc[i]`
- [ ] μ is computed on the training slice only — not on the full sample
- [ ] Baseline metrics committed to `runtime/benchmarks/baseline.json`
- [ ] No external API import in the notebook
