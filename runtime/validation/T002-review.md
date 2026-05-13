# Review Report — T002

**Reviewer role:** Critical Reviewer  
**Artifact:** analysis.ipynb § 2 (cells 9–15) + runtime/benchmarks/baseline.json  
**Date:** 2026-05-13  
**Verdict:** APPROVE

---

## Anti-pattern audit

### 1. Look-ahead bias / data leakage — PASS

**`sn_a()` (cell 11, line ~228):** Returns `float(series.iloc[t - 4])`. Since `t - 4 < t` for all valid `t`, only a past index is read. Guard `if t < 4: return nan` prevents any undefined access. ✓

**`sn_b()` (cell 11, line ~242):** Inner loop is `for j in range(4, t)`, i.e. j ∈ {4, 5, …, t-1}. Every `series.iloc[j]` and `series.iloc[j-4]` is strictly before index `t`. The final return likewise uses `series.iloc[t - 4]`. No forward reference anywhere. ✓

**OOS loop (cell 12, line ~282):** `for t in range(INITIAL_TRAIN, n)` — starts at index 16. At each iteration only indices ≤ t-1 are passed into the prediction functions before `actual = revenue_series.iloc[t]` is recorded for error computation. ✓

**Manual trace — first OOS fold:**
- `t = 16` (INITIAL_TRAIN)
- Target quarter date: `2014-01-31` (Walmart FY2014 Q1, Nov 2013–Jan 2014)
- Start of quarter: `2013-11-01` → `decision_date(t) = 2013-10-31`
- `sn_a` reads `series.iloc[12]` = the quarter ending `2013-01-31` (exactly 4 quarters back)
- Publication lag: `2013-01-31 + 45 days ≈ 2013-03-17`
- `2013-03-17 << 2013-10-31` → data was available before the decision date ✓
- No look-ahead in the first fold, and by induction the property holds for all subsequent folds.

### 2. Train/test contamination — PASS

In cell 12, `pred_sna = sn_a(revenue_series, t)` and `pred_snb = sn_b(revenue_series, t)` are computed *before* `actual = revenue_series.iloc[t]` is looked up. The target value `actual` is used only to compute the error *after* the prediction is made; it is never passed into any prediction function. `sn_a` and `sn_b` accept the full series but read only indices < t, so the target is never an input to the baseline formula. No observation appears in both training history and OOS target at the same fold. ✓

### 3. Improper time-series cross-validation — PASS

A global grep of the notebook reveals no `KFold`, `ShuffleSplit`, `StratifiedKFold`, `train_test_split`, `sample()`, or any randomised splitter.

`TimeSeriesSplit` is imported in cell 12 with `# noqa: F401 — imported to confirm availability`. It is **not instantiated** and **not used** as a splitter. The actual split is a forward-rolling expanding-window hand-rolled loop (`for t in range(INITIAL_TRAIN, n)`, step 1), which is correct and forward-only. The comment in cell 12 explicitly states: *"TimeSeriesSplit does NOT shuffle; shuffle=False is the ONLY valid setting for time-series."* The `(or equivalent forward-rolling)` clause in the acceptance criteria is satisfied. ✓

### 4. In-sample metric reporting — PASS

All metrics in cell 13 (MAPE, RMSE for SN-A and SN-B) are derived from `oos_df`, which is constructed exclusively from the OOS loop in cell 12. No in-sample R², in-sample accuracy, or any fitted statistic appears as a result anywhere in cells 10–14. The `oos_df` variable is created only from `oos_rows`, which accumulate only for `t ≥ INITIAL_TRAIN`. ✓

### 5. Baseline omission — PASS

- **SN-A** (`Q_hat(t) = Q(t-4)`) is defined in cell 11 with a full docstring stating the formula and causal guarantee. It is reported as the headline metric in cell 13 with the label "SN-A (Q(t-4))".
- **SN-B** (`Q_hat(t) = Q(t-4) * (1 + g_bar)`) is also defined in cell 11 with a full docstring. It is reported in cell 13 with an explicit label "[robustness check]".
- Cell 15 (terminal markdown) states: *"The SN-A baseline MAPE establishes the bar that FRED-based models (T004) must clear."* Ordering and role of each formulation are unambiguous. ✓

### 6. Structural-break blindness — PASS

Cell 13 constants:
```python
PANDEMIC_START = pd.Timestamp("2020-01-31")  # Walmart FY2020 Q1 end
PANDEMIC_END   = pd.Timestamp("2021-01-31")  # Walmart FY2021 Q1 end
```

These match methodology.md § 8 verbatim ("2020Q1–2021Q1" in Walmart fiscal calendar: FY2020 Q1 ends Jan 31 2020, FY2021 Q1 ends Jan 31 2021).

Pandemic quarter count: `oos_df["date"].between(PANDEMIC_START, PANDEMIC_END)` is inclusive on both ends, capturing quarters 2020-01-31, 2020-04-30, 2020-07-31, 2020-10-31, 2021-01-31 = **5 quarters**. Confirmed by `full_sample.n_quarters = 49` minus `pandemic_excluded.n_quarters = 44 = 5`. `pandemic_n` is printed in cell 13. ✓

Both full-sample and pandemic-excluded MAPE and RMSE are reported for SN-A. ✓

---

## Project-specific checks

| Check | Result | Evidence |
|---|---|---|
| FRED not referenced in §2 cells | **YES** | Cell 10 uses only `wmt_raw`. Cells 11–14 contain no `fred_raw`, `fred_cq`, `retail_sales_fred`, or any FRED variable reference. FRED variables exist in kernel memory from §1 but are never accessed in §2. |
| Both formulations documented | **YES** | `sn_a()` and `sn_b()` both have multi-line docstrings including formula, causal guarantee, args, and return. Cell 11, lines 222–264. |
| OOS initial train ≥ 16 quarters | **YES** | `INITIAL_TRAIN = 16` declared at cell 12, line ~280. First OOS fold is t=16. |
| Per-quarter error table in baseline.json | **YES** | JSON `per_quarter` array contains 49 entries from 2014-01-31 through 2026-01-31, each with `date`, `actual`, `pred_sna`, `pred_snb`, `err_sna`, `err_snb`, `ape_sna`, `ape_snb`. |
| MAPE and RMSE in JSON under sna | **YES** | `sna.full_sample.MAPE = 0.033131`, `sna.full_sample.RMSE = 6266657907.25`, `sna.pandemic_excluded.MAPE = 0.031148`, `sna.pandemic_excluded.RMSE = 6119122261.4`. All four keys present. |
| JSON schema compatibility for T004 | **YES** | Keys `sna.full_sample.MAPE`, `sna.pandemic_excluded.MAPE`, `sna.full_sample.RMSE`, `sna.pandemic_excluded.RMSE` are all present and correctly typed. |
| Pandemic window definition | **YES** | `PANDEMIC_START = 2020-01-31`, `PANDEMIC_END = 2021-01-31`. Matches methodology.md § 8 and the JSON `pandemic_window` block. |

---

## Findings

### BLOCKERs
None.

### MAJORs
None.

### MINORs
None.

### NITs

**NIT-1 — `TimeSeriesSplit` imported but never instantiated (cell 12)**  
The import is decorated with `# noqa: F401 — imported to confirm availability`. This is an unusual pattern that may confuse downstream readers or static analysis. The hand-rolled loop is correct; the NIT is cosmetic. *No fix required for APPROVE.*

**NIT-2 — SN-B RMSE absent from baseline.json**  
`snb.full_sample` and `snb.pandemic_excluded` carry only `MAPE`, not `RMSE`. SN-A is the headline metric and carries full MAPE + RMSE; SN-B is a robustness check. The acceptance criteria's RMSE requirement applies to the headline (SN-A). Recommend adding SN-B RMSE when T004 comparisons are assembled, for symmetry. *No fix required for APPROVE.*

**NIT-3 — Methodology §7 terminology vs. implementation**  
Methodology §7 says "MAPE on YoY growth *predictions*". The code computes APE as `|Q(t) - Q(t-4)| / |Q(t)|`, i.e., a level-based MAPE. For SN-A this is numerically equivalent to the absolute actual YoY growth rate (since the predicted YoY growth is 0%), and the 3.31% result is meaningful. However, a literal "MAPE on the growth-rate prediction" would yield MAPE = 100% for every SN-A quarter (since SN-A always predicts 0% growth). The implementation is correct and standard; the methodology text is slightly loose. *No fix required for APPROVE; flag for methodology.md cleanup.*

---

## Summary

All six anti-pattern audit items pass with positive evidence. Every project-specific acceptance criterion is satisfied. The OOS loop is strictly forward-rolling with INITIAL_TRAIN = 16, no shuffling, no FRED contamination, and the pandemic exclusion window correctly spans the 5 Walmart fiscal quarters from 2020-01-31 through 2021-01-31. No BLOCKERs or MAJORs were identified. The artifact is clean and the JSON schema is T004-ready.

**Verdict: APPROVE — T002 is cleared. Director may mark T002 DONE.**
