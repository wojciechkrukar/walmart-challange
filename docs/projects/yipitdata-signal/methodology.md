# Methodology — YipitData Signal Validation

> The how. Every step here exists to enforce one of the five mission-directive guardrails in
> `challenge-brief.md`. The Critical Reviewer audits each step against this document.

## 1. Data ingestion

- Read the two CSVs from `data/` only. Verify SHA-256 hashes against `data-contracts.md`.
- Parse `date` as a Pandas `DatetimeIndex` for both series.
- Walmart fiscal-quarter ends are kept as-is (last day of January / April / July / October).

## 2. Frequency alignment

The customer question is **quarterly**, so the joint frame is quarterly:

- `walmart_revenue.csv` is already quarterly. Compute YoY growth as `value / value.shift(4) - 1`.
- `retail_sales_fred.csv` is monthly. Aggregate to a Walmart-aligned fiscal quarter by summing
  the three constituent months. Compute YoY growth on the aggregated quarter.
- The aggregation MUST respect Walmart's fiscal calendar (Feb–Apr is fiscal-Q1, etc.). Calendar
  quarters introduce a one-month misalignment that has bitten previous candidates.

## 3. Publication-lag rule (zero look-ahead)

This is the most failure-prone step. The Reviewer audits it on every Task.

- For each prediction target quarter `Q`, define the **decision date** as `start(Q) - 1 day`.
- A predictor is allowed only if its physical release date `<=` decision date.
- Walmart revenue: a value with `date == quarter_end(Q-1)` becomes available `~45 days` after
  `quarter_end(Q-1)`. For most fiscal calendars that is well before `start(Q+1)` but **not**
  necessarily before `start(Q)`. Use only `Q-2` and earlier for any feature based on Walmart's
  own historical revenue.
- FRED RSXFS: a value with `date == month_start(m)` becomes available `~45 days` after
  `month_end(m)`. For each prediction quarter `Q`, the most recent FRED month usable as a
  feature is the latest month whose release date `<=` decision date.
- Implementation pattern: build a `feature_release_calendar` table, then `merge_asof(direction="backward")`
  with a tolerance and an explicit cutoff.

## 4. Seasonal Naive Baseline (built FIRST)

Two equivalent formulations — pick one and stick with it:

- **SN-A**: `Q_hat(t) = Q(t-4)` — naive same-quarter-last-year.
- **SN-B**: `Q_hat(t) = Q(t-4) * (1 + g_bar)` where `g_bar` is the trailing-N-quarters average YoY growth available at the decision date for quarter `t`. This is the brief's own example.

The baseline is computed quarter-by-quarter using only data available at the decision date for
that quarter. Its OOS errors are the bar that the FRED-based model must clear.

## 5. Alternative model (FRED signal)

Pick one or two simple models. Recommended starting set:

- **M1**: OLS regression of `revenue YoY` on `RSXFS YoY` at the appropriate publication lag (the
  brief's "first-pass" model, but with the publication-lag rule applied).
- **M2**: Augment M1 with the Seasonal Naive forecast as an explicit second regressor — i.e.,
  test whether FRED adds **incremental** information beyond what SN already captures.

Avoid temptation to throw kitchen-sink models at it. The brief explicitly says: pick one or two,
do them well.

## 6. Cross-validation (forward-rolling only)

- **No** `KFold`, `ShuffleSplit`, or any randomised splitter.
- Use `sklearn.model_selection.TimeSeriesSplit` or hand-rolled `expanding-window` / `rolling-window` splits.
- Initial train size: at least 16 quarters (4 years) so the first fit has ≥ 4 samples per
  seasonal cycle.
- Step size: 1 quarter. Predict the next quarter; record the OOS error; advance.

## 7. Headline metrics

- Primary: **OOS MAPE** on YoY growth predictions (matches the brief's "X percent" framing).
- Secondary: **OOS RMSE** on YoY growth predictions (less sensitive to small denominators in
  pandemic quarters).
- Per-quarter error tables go into `runtime/benchmarks/` for the Reviewer to inspect.

## 8. Structural-break handling (2020 COVID)

The brief is explicit: "Do not blindly fit a line through 2020." Concrete rules:

- Report the headline metric in **two cuts**: full sample, and excluding `2020Q1–2021Q1` (the
  acute disruption period).
- If a regression model is fit, include either:
  (a) a regime dummy `is_pandemic_quarter`, or
  (b) a separate sub-sample fit excluding the regime, with both reported in the memo.
- Plot the YoY series with the disruption period shaded so the reader sees the regime visually.

## 9. Causal "why"

The memo MUST address: is FRED RSXFS plausibly driving Walmart revenue, or are both proxies for
a common consumer-spending factor? At minimum, name the common factor and explain why the
relationship would or would not be expected to hold across regimes.

## 10. Falsifiable claim

The memo's headline must be falsifiable. Examples of well-formed claims:

- "FRED RSXFS YoY growth, lagged one publication cycle, beats the seasonal-naive baseline by
  X.X pp on out-of-sample MAPE across 2014Q1–2026Q1, but the gap collapses to Y.Y pp once the
  2020 disruption is excluded."
- "FRED RSXFS does not beat the seasonal-naive baseline at any tested lag; the evidence that
  would change our minds is a sustained ≥ 2 pp MAPE improvement on a held-out 2-year window."
