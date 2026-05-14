# Signal Validation Memo — Walmart Revenue vs. FRED RSXFS

**Customer question:** Does FRED RSXFS retail-sales data predict Walmart's quarterly revenue better than a simple baseline? If yes, by how much? What should we worry about?

## Bottom line up front

Yes. Over 42 genuine out-of-sample quarters (2015 Q3 – 2026 Q1), a simple model using FRED's monthly retail-sales index cut the average forecast error from **3.64% to 2.57%** — a gain of **1.07 percentage points** — with a 95% confidence interval of [+0.41 pp, +1.65 pp], sitting entirely above zero (§ 4 — see notebook).

## Method in one paragraph

MAPE — mean absolute percentage error — measures how wrong a forecast is, on average, as a share of the actual value; lower is better. The baseline is "Seasonal Naive" (SN-A): predict this quarter's revenue growth equals the same quarter one year ago. That is the bar any more-sophisticated model must beat. Model M1 runs an ordinary-least-squares regression of Walmart's year-over-year revenue growth on the FRED RSXFS retail-sales index, also expressed as year-over-year growth. To prevent peeking at the future, FRED data was restricted to readings that would have been publicly available roughly 45 days after each quarter's close, and the model was retrained one quarter at a time rolling forward — never on data from the quarter being forecast (§ 3, § 4 — see notebook).

## The numbers

| | SN-A baseline | M1 (FRED OLS) | Improvement |
|---|---|---|---|
| OOS MAPE — 42 qtrs (2015Q3–2026Q1) | 3.64% | 2.57% | **+1.07 pp** |
| 95% bootstrap CI | — | — | [+0.41, +1.65 pp] |
| OOS MAPE — excl. pandemic (37 qtrs) | 3.45% | 2.28% | **+1.17 pp** |
| 95% CI excl. pandemic | — | — | [+0.52, +1.74 pp] |

_(Sources: § 4, § 5 — see notebook; runtime/benchmarks/oos_errors.json. SN-A figures restricted to the same window as M1 for a fair comparison.)_

The improvement is consistent and statistically distinguishable from noise on both cuts.

## What to worry about

1. **Lag approximation.** We assume FRED data releases 45 days after each month-end, matching the documented FRED schedule. If FRED releases earlier in practice, the effective signal window is slightly wider and results could look mildly optimistic (§ 3 — see notebook).
2. **Common factor, not causation.** FRED RSXFS tracks total US retail sales, of which Walmart is a large constituent. Part of the predictive power may reflect Walmart's own mass — we are partly predicting a series from a sum it belongs to. The improvement is real, but it does not imply independent economic intelligence.
3. **2020 regime break.** During the pandemic, FRED retail sales fell sharply while Walmart revenue held flat or rose (essential-goods demand). The OLS beta between the two series collapsed to near zero over those five quarters. We report results both with and without this window; the signal survives either way, but a future disruption of similar character could neutralise it entirely (§ 5 — see notebook).
4. **Small sample.** 42 quarters is roughly ten years of data. Confidence intervals are wide. Anchoring on a point estimate of 1.07 pp is appropriate — treating it as precise is not.

## What would change our minds

If a fresh held-out window of at least eight quarters beginning no earlier than 2026 Q2 produces an M1 OOS MAPE improvement of less than 0.25 pp over SN-A, we would conclude the signal has degraded and recommend withdrawing the product.
