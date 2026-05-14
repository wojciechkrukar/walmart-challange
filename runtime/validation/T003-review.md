# Review Report — T003

**Reviewer role:** Critical Reviewer  
**Artifact:** analysis.ipynb § 3 (cells 15–23)  
**Date:** 2026-05-13  
**Verdict:** APPROVE

---

## Anti-pattern audit

**1. Look-ahead bias / data leakage — PASS**
The merge is `merge_asof(direction="backward", left_on="decision_date", right_on="feature_release_date")`. For every row in the merged frame, the FRED quarter used has `feature_release_date <= decision_date`. A hard `assert len(bad_rows) == 0` (cell 21, `#VSC-6385cf2b`) fires immediately if violated. The assertion passed for all 65 merged rows. Three quarters are spot-checked by hand below (§ Technical check 3). No other time-ordered join exists in § 3; the section contains no model fitting.

**2. Train/test contamination — N/A**
§ 3 performs data preparation only. No train/test split or model fitting is present.

**3. Improper time-series cross-validation — N/A**
No cross-validation in § 3. `KFold`, `ShuffleSplit`, and `train_test_split` are absent from these cells.

**4. In-sample metric reporting — N/A**
No metrics of any kind are computed in § 3. Confirmed: no `score()`, no `R²`, no MAPE, no RMSE.

**5. Baseline omission — N/A**
§ 3 is the merge step, not a modelling step. Baseline comparison belongs to T002/T004.

**6. Structural-break blindness — N/A**
No model is fit in § 3. Confirmed: no call to `fit()` or any estimator. The 2020 regime handling requirement applies only to §§ 4–5.

---

## T003-specific technical checks

### 1. Fiscal-quarter alignment

The `assign_fiscal_quarter()` function (cell 17, `#VSC-d23a8300`) was traced by re-running the logic against the raw data.

| Input month | Year rule applied | (fiscal_year, fq) returned | Correct? |
|---|---|---|---|
| January 2011 | `y - 1` | `(2010, 4)` | ✓ |
| February 2011 | `y` | `(2011, 1)` | ✓ |
| April 2011 | `y` | `(2011, 1)` | ✓ |
| November 2011 | `y` | `(2011, 4)` | ✓ |
| December 2011 | `y` | `(2011, 4)` | ✓ |

The docstring mapping (`Feb→fQ1, May→fQ2, Aug→fQ3, Nov/Dec/Jan→fQ4`) matches the documented Walmart fiscal calendar exactly. January correctly maps to `(year-1, 4)`. **No misalignment found.**

The `fiscal_quarter_end()` helper returns `Timestamp(fy, 4, 30)` for fQ1, `Timestamp(fy, 7, 31)` for fQ2, `Timestamp(fy, 10, 31)` for fQ3, and `Timestamp(fy+1, 1, 31)` for fQ4 — consistent with Walmart's fiscal calendar.

Only complete quarters (3 months present) are retained.

### 2. Publication-lag rule

Evidence from cell 19 (`#VSC-cdeed9a0`):

```python
fred_quarterly["last_month_end"] = fred_quarterly["last_month_in_quarter"] + MonthEnd(0)
fred_quarterly["feature_release_date"] = fred_quarterly["last_month_end"] + pd.Timedelta(days=45)
```

- `last_month_in_quarter` is the `max("date")` within each fiscal-quarter group — the last calendar month in that FRED fiscal quarter (FRED stores dates as month-start; `MonthEnd(0)` correctly maps these to month-end).
- `feature_release_date = last_month_end + 45 days`. For Walmart's fiscal quarters the last calendar month-end coincides with `fq_end` (April 30, July 31, October 31, January 31), so the distinction between `last_month_end` and `fq_end` is moot here — both yield the same result — but the code correctly implements the spec (`last_month_end`).
- Verified across 8 representative quarters: `feature_release_date` matches `last_month_end + 45` in every case.

The merge in cell 21 (`#VSC-6385cf2b`):

```python
merged = pd.merge_asof(
    wmt_for_merge,
    fred_for_merge,
    left_on="decision_date",
    right_on="feature_release_date",
    direction="backward",
)
```

- `direction="backward"` selects the largest `feature_release_date` ≤ `decision_date`. ✓
- `left_on="decision_date"`, `right_on="feature_release_date"`. ✓

The hard assertion immediately follows:

```python
bad_rows = merged[merged["feature_release_date"] > merged["decision_date"]]
assert len(bad_rows) == 0, f"LOOK-AHEAD VIOLATION: ..."
```

Assertion passed. All 65 rows satisfy `feature_release_date <= decision_date`.

`decision_date` is computed in cell 20 (`#VSC-f859937f`) as `fq_start - 1 day`, where `fq_start` is derived from `fq_end` via `fiscal_quarter_start()`:

```python
if m == 4:    return pd.Timestamp(y, 2, 1)    # fQ1 starts Feb 1
elif m == 7:  return pd.Timestamp(y, 5, 1)    # fQ2 starts May 1
elif m == 10: return pd.Timestamp(y, 8, 1)    # fQ3 starts Aug 1
elif m == 1:  return pd.Timestamp(y-1, 11, 1) # fQ4 starts Nov 1
```

All four branches correct. `decision_date = fq_start - 1 day` as specified. ✓

### 3. Manual spot-check (3 quarters)

The verification script replicated the full § 3 pipeline from raw CSVs and extracted the three target rows.

---

**Row 1 — Walmart fQ3 FY2012 (date = 2011-10-31)**

| Field | Value | Expected | Match? |
|---|---|---|---|
| `decision_date` | 2011-07-31 | start(fQ3 FY2012) − 1d = Aug 1 − 1d = Jul 31 | ✓ |
| FRED quarter used (`fq_end`) | 2011-04-30 | fQ1 FY2011 | ✓ |
| `feature_release_date` | 2011-06-14 | Apr 30 + 45 d = Jun 14 | ✓ |
| lag satisfied (`frd ≤ dec`) | Jun 14 ≤ Jul 31 | True | ✓ |
| `rsxfs_yoy` | 0.074050 | 0.074050 | ✓ |
| `revenue_yoy` | 0.081156 | 0.081156 | ✓ |

Next FRED quarter (fQ2 FY2011, ends Jul 31 2011): release = Jul 31 + 45 = Sep 14 2011 > Jul 31 2011 — correctly excluded.

---

**Row 2 — Walmart fQ4 FY2012 (date = 2012-01-31)**

| Field | Value | Expected | Match? |
|---|---|---|---|
| `decision_date` | 2011-10-31 | start(fQ4 FY2012) − 1d = Nov 1 − 1d = Oct 31 | ✓ |
| FRED quarter used (`fq_end`) | 2011-07-31 | fQ2 FY2011 | ✓ |
| `feature_release_date` | 2011-09-14 | Jul 31 + 45 d = Sep 14 | ✓ |
| lag satisfied | Sep 14 ≤ Oct 31 | True | ✓ |
| `rsxfs_yoy` | 0.081043 | 0.081043 | ✓ |
| `revenue_yoy` | 0.058517 | 0.058517 | ✓ |

Next FRED quarter (fQ3 FY2011, ends Oct 31 2011): release = Oct 31 + 45 = Dec 15 2011 > Oct 31 2011 — correctly excluded.

---

**Row 3 — Walmart fQ1 FY2013 (date = 2012-04-30)**

| Field | Value | Expected | Match? |
|---|---|---|---|
| `decision_date` | 2012-01-31 | start(fQ1 FY2013) − 1d = Feb 1 − 1d = Jan 31 | ✓ |
| FRED quarter used (`fq_end`) | 2011-10-31 | fQ3 FY2011 | ✓ |
| `feature_release_date` | 2011-12-15 | Oct 31 + 45 d = Dec 15 | ✓ |
| lag satisfied | Dec 15 ≤ Jan 31 | True | ✓ |
| `rsxfs_yoy` | 0.077461 | 0.077461 | ✓ |
| `revenue_yoy` | 0.083617 | 0.083617 | ✓ |

Next FRED quarter (fQ4 FY2011, ends Jan 31 2012): release = Jan 31 + 45 = Mar 16/17 2012 > Jan 31 2012 — correctly excluded.

**All three spot-checks pass. Values match the Review Request's reference table exactly.**

### 4. Revenue look-ahead check

- `fred_for_merge` contains: `['fq_end', 'feature_release_date', 'rsxfs_fq_sum', 'rsxfs_yoy']`. No Walmart revenue column. ✓
- Revenue-related columns in the merged frame: `['revenue', 'revenue_yoy']`.
  - `revenue`: raw Walmart quarterly revenue, the prediction target.
  - `revenue_yoy`: computed after the merge as `merged["revenue"] / merged["revenue"].shift(4) - 1`. This is the TARGET column; it is not joined from any future period and is not used as a predictor in § 3.
- No `revenue.shift(-1)` or any negative shift exists in § 3.
- No join condition references future Walmart revenue.

**No revenue look-ahead. PASS.**

### 5. FRED YoY computed before merge

Cell 18 (`#VSC-7fee4bf6`) computes:

```python
fred_quarterly["rsxfs_yoy"] = (
    fred_quarterly["rsxfs_fq_sum"] / fred_quarterly["rsxfs_fq_sum"].shift(4) - 1
)
```

This cell executes on `fred_quarterly` BEFORE `fred_for_merge` is constructed and BEFORE `merge_asof` is called (cells 21–22). The YoY is therefore computed over the full FRED quarterly history in isolation. **PASS.**

---

## Acceptance-criteria checklist

| Criterion (from T003 Task Brief) | Result |
|---|---|
| FRED months aggregated to Walmart fiscal quarters using documented mapping | **PASS** |
| Explicit `decision_date` column computed as `start(Q) - 1 day` | **PASS** |
| Explicit `feature_release_date` column computed for FRED predictor | **PASS** |
| Merge logic is `merge_asof(direction="backward")` keyed on `feature_release_date <= decision_date` | **PASS** |
| Assertion confirms `feature_release_date <= decision_date` for every row, fails loudly if violated | **PASS** (65/65 rows) |
| Printed table shows first 5 prediction quarters with predictor values and release dates | **PASS** (cell 22, with MINOR caveat below) |
| Merged frame is in-memory only; no write to `data/` | **PASS** |

---

## Findings

### BLOCKERs
None.

### MAJORs
None.

### MINORs
None.

### NITs
**NIT-1 — Spot-check print table uses unfiltered frame (cell 22, `#VSC-cbb7d0ba`)**

The variable `spot_check` is correctly defined as `merged[...notna()...].head(5)` (filtering for rows where both YoY values are present), but the print statement uses `merged[display_cols].head(5)` — the unfiltered frame. For Walmart quarters earliest in the dataset where no FRED history exists, this printed table may display NaN FRED values that offer no human-eyeball utility. The `analysis_df` output is unaffected. Recommended fix: replace `merged[display_cols].head(5)` with `spot_check[display_cols]` in the print call.

---

## Summary

All five T003-specific technical checks pass: fiscal-quarter mapping is correct, publication-lag dates are computed from `last_month_end + 45 days`, the `merge_asof(direction="backward")` enforces the constraint, the hard assertion fires on every run and passed for all 65 rows, and the three mandated spot-check quarters reproduce the reference table exactly. There is no Walmart revenue look-ahead and no model fitting in § 3. One cosmetic NIT (unused `spot_check` variable in the print call) has no correctness impact.

**Verdict: APPROVE.**
