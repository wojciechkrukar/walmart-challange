## Task Brief

**Task ID:** T003
**Mission ID:** YIPIT-SIGNAL-001
**Title:** Walmart-fiscal aggregation + lag-aligned FRED merge
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** 1 (critical)
**Target milestone:** M3
**Depends on:** T002
**Status:** PENDING

### Objective

In `analysis.ipynb` § 3, aggregate the monthly FRED RSXFS series to Walmart's fiscal-quarter
boundary (Feb–Apr = fQ1, etc.) and merge it onto the Walmart revenue frame using the
publication-lag rule from `docs/projects/yipitdata-signal/methodology.md` § 3. The output is a
single in-memory dataframe of fiscal quarters with one column per legitimate predictor.

### Inputs

- The raw frames loaded in T001
- `docs/projects/yipitdata-signal/methodology.md` § 2 + § 3 (alignment + publication lag)

### Acceptance criteria

- [ ] FRED months are aggregated to Walmart fiscal quarters using the documented mapping.
- [ ] An explicit `decision_date` column is computed for each prediction quarter (`start(Q) - 1 day`).
- [ ] An explicit `feature_release_date` column is computed for each predictor (FRED + Walmart-lag features).
- [ ] The merge logic is `merge_asof(direction="backward")` (or equivalent) keyed on
      `feature_release_date <= decision_date`.
- [ ] An assertion confirms that for every row, every predictor's `feature_release_date` is `<=`
      that row's `decision_date`. The assertion fails loudly if violated.
- [ ] A small printed table shows, for the first 5 prediction quarters, the predictor values
      used and their release dates, so a human can eyeball the lag.
- [ ] The merged frame is **in-memory only**; no write back to `data/`.

### Out of scope

- Any model fitting (T004).
- Any structural-break work (T005).

### Forbidden

- Calendar-quarter aggregation of FRED (must be Walmart-fiscal).
- Forward-fill of FRED values past their actual release date.
- Using a Walmart revenue value to predict its own quarter (look-ahead — this is a BLOCKER).

### Reviewer audit focus (BLOCKER list)

- For each predicted quarter Q, every predictor must have `feature_release_date <= start(Q)`.
- Walmart revenue used as a predictor for Q must come from a fiscal quarter whose 10-Q filing
  date precedes `start(Q)`. Default conservative assumption: filing date `= quarter_end + 45 days`.
- The most recent FRED month usable for predicting Q is the latest month whose release date
  precedes `start(Q)`. Default conservative assumption: release date `= month_end + 45 days`.
- The Reviewer must spot-check at least three quarters by hand and document the check in the Review Report.
