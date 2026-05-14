## Task Brief

**Task ID:** T004
**Mission ID:** YIPIT-SIGNAL-001
**Title:** Forward-rolling OOS CV: FRED signal vs. baseline
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** 1 (critical)
**Target milestone:** M4
**Depends on:** T003
**Status:** PENDING

### Objective

In `analysis.ipynb` § 4, fit one or two simple alternative models that use the FRED signal
under the lag-aligned merge from T003. Compare them to the baseline from T002 on
**out-of-sample MAPE and RMSE**, with bootstrap 95% CIs on the headline delta. Report both the
full-sample and pandemic-excluded cuts.

### Inputs

- The merged frame from T003 (in-memory)
- `runtime/benchmarks/baseline.json` from T002
- `docs/projects/yipitdata-signal/methodology.md` § 5–7
- `docs/projects/yipitdata-signal/kpis.md`

### Recommended models (pick one OR both, not more)

- **M1**: OLS regression of `revenue_yoy` on `rsxfs_yoy_lagged`.
- **M2**: M1 augmented with the Seasonal Naive YoY forecast as a second regressor (tests
  whether FRED adds **incremental** information beyond what SN already captures).

### Acceptance criteria

- [ ] CV uses `TimeSeriesSplit` (or hand-rolled forward-rolling), `shuffle=False`, initial train ≥ 16 quarters, step = 1 quarter.
- [ ] Per-fold predictions and errors written to `runtime/benchmarks/oos_errors.json`.
- [ ] Headline `delta_MAPE = MAPE_baseline − MAPE_FRED_model` reported with a bootstrap 95% CI
      (≥ 1000 resamples over the OOS folds).
- [ ] Same headline reported on the pandemic-excluded cut (target quarters in 2020Q1–2021Q1 dropped).
- [ ] No `KFold`, `ShuffleSplit`, `StratifiedKFold`, or any randomised splitter anywhere.
- [ ] No in-sample R² presented as a result. (You MAY print it as a sanity check, clearly labelled "in-sample, not a result".)
- [ ] Each fit cell carries a one-line comment naming the regressors and the target.

### Out of scope

- The structural-break treatment (T005).
- Memo prose (T006).
- Polishing of figures (T006).

### Forbidden

- Reporting "X is better than Y" without a stated baseline definition matching T002.
- Reporting any result without a CI or DM-test statistic.
- Hyperparameter sweeps that touch the OOS folds (no leakage via tuning).

### Reviewer audit focus (BLOCKER list)

- The CV is forward-rolling. The Reviewer prints (or asks the Quant to print) the
  `(train_idx_max, test_idx)` pairs for at least 3 folds and confirms `train_idx_max < test_idx`.
- The bootstrap is over the OOS folds (paired by quarter), not over training rows.
- Pandemic-excluded cut is the same model fit on the same folds, with the offending target
  quarters dropped from the metric — not refit on a smaller window. (Or, if refit, this is
  documented and called out as a sensitivity.)
- The headline delta and CI in `oos_errors.json` match what the notebook prints.
