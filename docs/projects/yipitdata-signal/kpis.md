# KPIs — YipitData Signal Validation

## Mission KPI priority order (strict)

A lower-rank gain MUST NOT be traded for a higher-rank regression.

| # | KPI                                                | Target                                                        |
|---|----------------------------------------------------|---------------------------------------------------------------|
| 1 | **Anti-pattern audit pass rate**                  | 100% — every item in `docs/kernel/review_policy.md` § 6 addressed in writing |
| 2 | **Notebook reproducibility**                      | Restart-and-Run-All passes on a clean kernel                  |
| 3 | **Honest answer to the customer question**        | One of: "yes by X%", "no — here's the evidence that would change our mind" |
| 4 | **OOS error of FRED-based model vs. baseline**    | Reported as a level-equivalent MAPE delta (pp); see § "Out-of-sample error metrics" for the exact denominator |
| 5 | **Regime-aware reporting**                        | Headline number reported full-sample AND excluding 2020Q1–2021Q1 |

## Out-of-sample error metrics

### Primary: level-equivalent MAPE

The notebook scores all models on a **level-equivalent** Absolute Percentage Error so that the
T002 Seasonal Naive baseline and the T004 FRED-augmented models are compared on the same
denominator. For every prediction quarter *t*, define the level prediction
`Q_hat(t) = Q(t-4) * (1 + pred_yoy(t))` and write APE in revenue-level terms:

```
APE(t) = | Q(t) − Q_hat(t) | / Q(t)
       = | actual_yoy(t) − pred_yoy(t) | / ( 1 + actual_yoy(t) )      ← used in analysis.ipynb
```

The two lines are algebraically identical. The right-hand form is the one implemented in
`analysis.ipynb` (Cell 26, comment block at lines 1225–1230 and the `ape_m1` / `ape_m2`
computation at line 1269). For the SN-A baseline, `pred_yoy(t) = 0`, which collapses to the
T002 form `APE_sna(t) = |actual_yoy(t)| / (1 + actual_yoy(t)) = |Q(t) − Q(t−4)| / Q(t)`.

```
MAPE_oos = mean( APE(t) )   over OOS folds
```

Reported in percentage points. We compare:
- `MAPE_seasonal_naive` (baseline)
- `MAPE_fred_signal` (alternative)
- `delta = MAPE_seasonal_naive - MAPE_fred_signal`  ← positive ⇒ FRED helps

> **Why not divide by `|actual_yoy|`?** A YoY-denominator MAPE blows up whenever YoY growth
> is near zero (which happens every time Walmart's quarter is close to flat year-over-year),
> and the resulting number is not comparable to a level-based naive baseline. The
> level-equivalent denominator `(1 + actual_yoy)` is bounded away from zero for Walmart's
> revenue history (Walmart never went to zero revenue), and it makes the SN-A baseline
> formula and the FRED-model formula identical up to the prediction term.

### Secondary: RMSE

The T002 baseline (`runtime/benchmarks/baseline.json`, written by Cell 16) reports RMSE in
**revenue-level dollars** (`err_sna = Q(t) − Q_hat(t)`). The T004 FRED models
(`runtime/benchmarks/oos_errors.json`, written by Cell 35) report RMSE in **YoY-residual
units** (`err_m1 = actual_yoy − pred_yoy`). They are two different units and are not
directly comparable; the headline comparison uses the level-equivalent MAPE above. RMSE is
kept as a tiebreaker / sanity check within each cohort.

```
RMSE_baseline_levels = sqrt( mean( ( Q(t) − Q_hat(t) )^2 ) )           ← T002 baseline
RMSE_model_yoy       = sqrt( mean( ( actual_yoy(t) − pred_yoy(t) )^2 ) ) ← T004 FRED models
```

## Uncertainty quantification

Each headline delta MUST be reported with one of:
- A 95% bootstrap CI over the OOS folds (recommended).
- A paired Diebold-Mariano test statistic on the per-quarter squared errors.

A delta whose CI crosses zero is reported as **not statistically distinguishable from zero**,
not as "positive but small".

## Reporting cuts (mandatory)

Every headline number is reported twice:
1. **Full sample.**
2. **Pandemic-excluded** (drop predictions for any quarter overlapping 2020Q1–2021Q1).

If the two cuts disagree on the sign of `delta`, the memo MUST say so explicitly.

## Falsifiability requirement

A "yes, the signal beats the baseline" claim is admissible only if `delta > 0` in **both** cuts
with the bootstrap CI excluding zero in at least the pandemic-excluded cut.

A "no" answer is admissible only if `delta <= 0` in at least one cut, AND the memo specifies
exactly what evidence would update the answer to "yes" (e.g., "a sustained ≥ 2 pp MAPE
improvement on a forward 2-year window").
