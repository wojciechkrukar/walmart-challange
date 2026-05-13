# KPIs — YipitData Signal Validation

## Mission KPI priority order (strict)

A lower-rank gain MUST NOT be traded for a higher-rank regression.

| # | KPI                                                | Target                                                        |
|---|----------------------------------------------------|---------------------------------------------------------------|
| 1 | **Anti-pattern audit pass rate**                  | 100% — every item in `docs/kernel/review_policy.md` § 6 addressed in writing |
| 2 | **Notebook reproducibility**                      | Restart-and-Run-All passes on a clean kernel                  |
| 3 | **Honest answer to the customer question**        | One of: "yes by X%", "no — here's the evidence that would change our mind" |
| 4 | **OOS error of FRED-based model vs. baseline**    | Reported as MAPE delta (pp) and RMSE delta on YoY growth      |
| 5 | **Regime-aware reporting**                        | Headline number reported full-sample AND excluding 2020Q1–2021Q1 |

## Out-of-sample error metrics

### Primary: MAPE on YoY revenue growth

```
MAPE_oos = mean( | y_true - y_pred | / | y_true | )   over OOS folds
```

Reported in percentage points. We compare:
- `MAPE_seasonal_naive` (baseline)
- `MAPE_fred_signal` (alternative)
- `delta = MAPE_seasonal_naive - MAPE_fred_signal`  ← positive ⇒ FRED helps

### Secondary: RMSE on YoY revenue growth

```
RMSE_oos = sqrt( mean( (y_true - y_pred)^2 ) )   over OOS folds
```

Same delta convention. RMSE is the tiebreaker when MAPE is unstable in low-base quarters.

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
