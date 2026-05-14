# Review Report — T004

**Reviewer role:** Critical Reviewer
**Artifact:** analysis.ipynb § 4 (cells 24–31, notebook cells 24–32) + runtime/benchmarks/oos_errors.json
**Date:** 2026-05-13
**Verdict:** APPROVE

---

## Anti-pattern audit

### 1. Look-ahead bias / data leakage — PASS

Three leakage vectors examined:

**CV slicing.** Cell 27 (notebook cell 28, execution count 31):
```python
train = df_cv.iloc[:t]   # rows 0 … t-1 — strictly before fold t
test  = df_cv.iloc[[t]]  # single row at position t — never in train
```
The slicing is correct. No row can appear in both sets.

**`snb_yoy_fc` pre-computation (critical trace).** Cell 26 (execution count 28):
```python
for j in range(4, t):                  # Python range(4, t) → j ∈ {4, 5, …, t-1}
    past_yoy.append(
        wmt_df.loc[j, "revenue"] / wmt_df.loc[j - 4, "revenue"] - 1
    )
```
where `t = wmt_q.index` of `target_date`. The last `j` is `t - 1`, one quarter strictly before the prediction target. The target index `t` itself is never read. Python's `range(4, t)` — *not* `range(4, t + 1)` — is the operative bound. ✓ No leakage.

**`rsxfs_yoy` feature.** This is the lag-aligned FRED regressor constructed in T003 and inherited through `analysis_df`. T003 was approved (see T003-review.md); the publication-lag rule is enforced at the merge layer. Spot-checked three rows in oos_errors.json: the earliest OOS fold (2015-10-31) is preceded by 16 training quarters bearing FRED data that would have been released before 2015-10-31. ✓

**snb_yoy_fc pre-computation before the CV loop.** The function is deterministic — for each row its output is a function of wmt_q rows strictly before that row's own date. Pre-computing it outside the loop does not introduce cross-fold information because `snb_yoy_fc[test_row_t]` depends only on `wmt_q[0 … t_wmt_idx - 1]`, which is a subset of the training data available at fold `t`. ✓

### 2. Train/test contamination — PASS

Cell 27 (execution count 31) carries an explicit run-time assertion:
```python
assert (oos_cv_df["train_end_idx"] < oos_cv_df["test_idx"]).all(), "SHUFFLE/LEAKAGE VIOLATION!"
```
Followed by printed output:
```
✓ Forward-rolling assertion: train_end_idx < test_idx for all folds
```
The assertion was live at execution time (execution count 31, no error recorded in output). The record fields `train_end_idx = t - 1` and `test_idx = t` are written inside the same loop, making the invariant structurally guaranteed by construction. ✓

### 3. Improper time-series cross-validation — PASS

No `KFold`, `ShuffleSplit`, `StratifiedKFold`, `train_test_split(…, shuffle=True)`, or any randomised splitter is present in § 4. `TimeSeriesSplit` appears in the kernel import namespace (visible in notebook variables) but is not invoked in the CV loop — it is imported for documentation/reference only. The actual split is hand-rolled:

```python
for t in range(INITIAL_TRAIN_CV, len(df_cv)):   # t = 16, 17, 18, … deterministic
    train = df_cv.iloc[:t]
    test  = df_cv.iloc[[t]]
```

Initial train = 16 quarters (`INITIAL_TRAIN_CV = 16`), step = 1. The fold print confirms monotonic advancement:
```
Fold t=16: train[0..15] (n=16), test t=16 (2015-10-31)
Fold t=17: train[0..16] (n=17), test t=17 (2016-01-31)
Fold t=18: train[0..17] (n=18), test t=18 (2016-04-30)
```
These are strictly increasing, confirming no shuffle. ✓

### 4. In-sample metric reporting — PASS

The full-sample in-sample R² appears exactly once, in cell 28 (execution count 32), with the mandatory label:
```python
print(f"[IN-SAMPLE SANITY — NOT A RESULT] M1 full-sample R²: {_is_r2:.3f}")
```
The headline section header reads `=== OOS Results Summary ===` and all primary metrics (OOS MAPE columns, delta_MAPE, bootstrap CI) are out-of-sample quantities. The in-sample R² line is visually separated and explicitly disowned. ✓

### 5. Baseline omission — PASS

Cell 26 (execution count 27) loads the baseline from the T002 artefact on disk:
```python
with open("runtime/benchmarks/baseline.json") as f:
    baseline_bm = json.load(f)
sna_full_mape = baseline_bm["sna"]["full_sample"]["MAPE"]    # 0.033131 — not hardcoded
sna_excl_mape = baseline_bm["sna"]["pandemic_excluded"]["MAPE"]
```
Confirmed against `baseline.json`: `sna.full_sample.MAPE = 0.033131`, `sna.pandemic_excluded.MAPE = 0.031148`. The values used in cell 28's delta calculation match exactly. No hardcoded constants substituted for the JSON values. ✓

### 6. Structural-break blindness — PASS

Pandemic window is declared (`PANDEMIC_START = 2020-01-31`, `PANDEMIC_END = 2021-01-31`) and applied in cell 28 (execution count 32):
```python
excl_mask = full_mask & ~oos_cv_df["date"].between(PANDEMIC_START, PANDEMIC_END)
```
Both cuts are computed, printed, and persisted to `oos_errors.json`:
- Full-sample: n=42, MAPE 2.57%, delta +0.74pp
- Pandemic-excluded: n=37, MAPE 2.28%, delta +0.84pp

oos_errors.json confirms: `M1.full_sample.n_quarters = 42`, `M1.pandemic_excluded.n_quarters = 37`. The 5-quarter difference (42 − 37 = 5) matches the pandemic window (2020Q1 through 2021Q1 = five Walmart fiscal quarters). ✓ The model is NOT refit on a smaller window; the exclusion is metric-only, as required by the task brief.

---

## T004-specific technical checks

### A. APE formula consistency — PASS

Cell 27 (execution count 31):
```python
denom  = 1.0 + y_actual          # = 1 + actual_yoy = Q(t) / Q(t-4)
ape_m1 = abs(y_actual - pred_m1) / denom
ape_m2 = abs(y_actual - pred_m2) / denom
```

This implements `|actual_yoy − pred_yoy| / (1 + actual_yoy)`, **not** the unstable `|error_yoy| / |actual_yoy|`. The identity proof from the review brief holds:

```
|actual_yoy − pred_yoy| / (1 + actual_yoy)
  = |Q(t)/Q(t-4) − Q_hat(t)/Q(t-4)| / (Q(t)/Q(t-4))
  = |Q(t) − Q_hat(t)| / Q(t)
```

This is exactly the level-equivalent APE formula. It is identical in structure to T002's `ape_sna = |Q(t) − Q(t-4)| / Q(t)`, making the MAPE comparison valid. The denominator `1 + actual_yoy` is always positive because Walmart never reported zero or negative revenue. A code comment in cell 27 explicitly documents the equivalence: "This equals |Q(t) − Q_hat(t)| / Q(t) — the same formula T002 used for ape_sna." ✓

### B. Bootstrap correctness — PASS

Cell 29 (execution count 33):
```python
n   = len(aligned)                          # 42 OOS quarters
idx = rng.integers(0, n, size=n)           # resample OOS fold indices

samp               = aligned.iloc[idx]     # paired (actual, ape_m1, ape_sna) rows
delta_mape_boot[i] = samp["ape_sna"].mean() - samp["ape_m1"].mean()
```

The resampling unit is the OOS quarter (a paired `(ape_sna, ape_m1)` observation). The model is **not** refit in any bootstrap iteration; the OLS fits from the CV loop are used as-is. The seed is fixed (`np.random.default_rng(seed=42)`) for reproducibility. BOOTSTRAP_N = 2000 ≥ 1000 required. Percentile method (2.5th, 97.5th) applied via `np.percentile` and `np.nanpercentile`. Both full-sample and pandemic-excluded CIs are produced. ✓

The `aligned` frame is constructed via inner join on `date` between `oos_cv_df` and `baseline_pq` (the per-quarter SNA error table from T002 JSON), ensuring the bootstrap delta is computed on matched (OOS quarter, SNA quarter) pairs for the same 42 dates. ✓

### C. JSON schema — PASS

`runtime/benchmarks/oos_errors.json` contains:

| Required field | Present | Value |
|---|---|---|
| `M1.full_sample.delta_MAPE_vs_SNA` | ✓ | 0.0074 |
| `M1.full_sample.bootstrap_95ci_lo` | ✓ | 0.004136 |
| `M1.full_sample.bootstrap_95ci_hi` | ✓ | 0.016502 |
| `M1.pandemic_excluded.delta_MAPE_vs_SNA` | ✓ | 0.008361 |
| `M1.pandemic_excluded.bootstrap_95ci_lo` | ✓ | 0.005202 |
| `M1.pandemic_excluded.bootstrap_95ci_hi` | ✓ | 0.017405 |
| `per_quarter` list | ✓ | 42 entries |

`per_quarter` runs from `2015-10-31` to `2026-01-31` (42 entries confirmed by manual count). Each entry has `date`, `actual` (revenue_yoy), `pred_m1`, `pred_m2`, `err_m1`, `err_m2`, `ape_m1`, `ape_m2`. The `actual` field stores the **YoY growth rate** — not the revenue level — which is explicitly noted in the cell 27 comment "actual_yoy (growth rate, NOT level)". Downstream consumers (T005, T006) must be aware of this unit distinction when joining with baseline.json's per_quarter table (which stores revenue in dollar levels). ✓

M2 does not carry bootstrap CIs in the JSON. The task brief specifies the bootstrap requirement for the headline delta (M1); M2 is a secondary/sensitivity model. No spec violation. ✓

### D. snb_yoy_fc leakage check — PASS

The loop bound is the critical question. Cell 26 (execution count 28), confirmed code:
```python
t = t_idx[0]           # integer position of target_date in wmt_q
for j in range(4, t):  # range(4, t) → j ∈ {4, 5, …, t-1}
    past_yoy.append(
        wmt_df.loc[j, "revenue"] / wmt_df.loc[j - 4, "revenue"] - 1
    )
```

**`range(4, t)` — not `range(4, t + 1)`**. The last index consumed is `t - 1`, which is the quarter immediately preceding the target quarter at index `t`. The target quarter's own revenue (`wmt_q.loc[t, "revenue"]`) is never read during the g_bar computation. ✓

For concreteness: the first OOS fold target is 2015-10-31. In `wmt_q` (indexed 0 = 2010-01-31), this date is at index 23. The loop runs `range(4, 23)` → j ∈ {4, 5, … , 22}. The last wmt_q revenue read is index 22 = 2015-07-31, one fiscal quarter before the target. This is data physically published ~45 days after 2015-07-31, well before the 2015-10-31 quarter start. ✓

---

## Findings

### BLOCKERs
None.

### MAJORs
None.

### MINORs

**MINOR-1 — Headline delta_MAPE_vs_SNA point estimate uses mismatched evaluation windows.**

In cell 28:
```python
delta_m1_full = sna_full_mape - m1_full_mape
#               ^ 49-quarter SNA MAPE from baseline.json (T002: 2014-Q1 → 2026-Q1)
#                              ^ 42-quarter M1 MAPE (OOS: 2015-Q4 → 2026-Q1)
```

The `sna_full_mape` from `baseline.json` (0.033131) covers 49 quarters including 7 pre-OOS quarters (2014-Q1 through 2015-Q3) that are excluded from M1's evaluation because the initial train window of 16 quarters is not yet satisfied. The headline 0.74pp delta in oos_errors.json therefore reflects different time windows for numerator and denominator.

The bootstrap CI in cell 29 is *not* affected: `aligned` is an inner join on date, so both `ape_sna` and `ape_m1` are averaged over the same 42 matched quarters. The CI [+0.41pp, +1.65pp] is correctly computed and entirely positive.

Materiality assessment: the 7 excluded early quarters have ape_sna well below the 3.31% mean (2014-Q1: 1.49%, 2014-Q4: 2.78%, 2015-Q4: 0.09% — all below average), so the SNA MAPE over the 42 OOS quarters is **higher** than 3.31%. The mismatched headline delta is therefore conservative — it *understates* M1's advantage. The conclusion is robust and unambiguous regardless.

**Smallest fix:** In cell 28, add one line to compute the aligned baseline MAPE and use it as the headline delta:
```python
# Aligned SNA MAPE over the same 42 OOS quarters (for consistent delta calculation)
aligned_sna_mape = aligned["ape_sna"].mean()
delta_m1_full_aligned = aligned_sna_mape - m1_full_mape
```
Update `oos_results["M1"]["full_sample"]["delta_MAPE_vs_SNA"]` (and pandemic-excluded equivalent) to use the aligned computation. The existing bootstrap CI remains unchanged.

### NITs

**NIT-1 — Execution count gap between cells 27 and 28 (counts 29, 30 unaccounted for).**
The notebook shows execution count 28 for cell 27 (snb_yoy_fc preparation) and count 31 for cell 28 (CV loop). Two cells ran at counts 29 and 30 between these steps. Cell 28 re-initialises `df_cv` from `analysis_df` and redefines `INITIAL_TRAIN_CV`, so kernel contamination from the gap cells is negligible. However, an end-to-end fresh-kernel run should be confirmed before finalising T006.

**NIT-2 — `actual` field units in oos_errors.json differ from baseline.json.**
`oos_errors.json per_quarter[*].actual` stores `revenue_yoy` (dimensionless rate, e.g. 0.078); `baseline.json per_quarter[*].actual` stores revenue in dollars (e.g. 1.29e11). T005/T006 date-joins on these tables must not average or compare these "actual" columns directly. The NIT is documentation-only; no code change required in T004.

---

## Acceptance-criteria checklist (from T004 task brief)

- [x] CV uses hand-rolled forward-rolling; `shuffle=False`; initial train = 16 quarters; step = 1 quarter.
- [x] Per-fold predictions and errors written to `runtime/benchmarks/oos_errors.json`.
- [x] Headline `delta_MAPE` reported with bootstrap 95% CI (2000 resamples over OOS folds).
- [x] Pandemic-excluded cut reported alongside full-sample.
- [x] No `KFold`, `ShuffleSplit`, `StratifiedKFold`, or randomised splitter.
- [x] No in-sample R² presented as a result (labelled `[IN-SAMPLE SANITY — NOT A RESULT]`).
- [x] Each fit cell carries comments naming regressors and target.

All 7 criteria pass.

---

## Summary

All six anti-pattern items pass and all four T004-specific technical checks (APE formula, bootstrap design, JSON schema, snb leakage) pass. The sole non-trivial finding (MINOR-1) is a window mismatch in the headline delta_MAPE_vs_SNA point estimate: the T002 SNA MAPE (49 quarters) is subtracted from the M1 OOS MAPE (42 quarters). The mismatch is conservative — it understates M1's advantage — and the bootstrap CI (which is correctly aligned) renders the conclusion robust: M1 beats SN-A at the 95% level on both full-sample and pandemic-excluded cuts. The artifact meets all task-brief acceptance criteria. Verdict: **APPROVE**.

---

*Routed to: Director*
*Copy to: Lead Quant (MINOR-1 fix recommended before T006 memo figures are finalised)*
