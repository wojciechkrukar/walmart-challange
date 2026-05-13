# Signal Validation Memo
**To:** Portfolio Manager
**From:** Quantitative Research Team
**Re:** Does FRED Retail Sales Predict Walmart Revenue?
**Date:** May 2026

---

## The Question

A client asked whether the U.S. monthly retail-sales index published by the
Federal Reserve (FRED series RSXFS) can serve as a *leading indicator* of
Walmart's quarterly revenue — and whether it beats the simplest possible
forecast one could make.

---

## Bottom Line Up Front

**In normal market conditions, yes — but only marginally, and COVID broke it.**

The lagged FRED signal beats a seasonal-naive baseline by roughly **36% on
MAPE** in the pre-COVID period (2014–2019). Over the full sample including
COVID, the signal does **not** reliably outperform the naive guess.

| Period | Seasonal Naive MAPE | FRED Signal MAPE | Winner |
|---|---|---|---|
| Pre-COVID (2014–2019) | 2.02% | 1.29% | **Signal** |
| COVID window (2020–2021) | 2.07% | 4.21% | Naive |
| Post-COVID (2022–2026) | 2.86% | 3.03% | Naive (slight) |
| **Full OOS** | **2.36%** | **2.49%** | **Naive** |

All numbers are strict out-of-sample (forward-rolling cross-validation, never
touching future data during training).

---

## The Methodology, Plain English

**Baseline:** "Next quarter will look like the same quarter last year, adjusted
for the typical year-over-year growth rate." That is the hardest bar to clear —
Walmart's revenue is deeply seasonal and grows steadily, so simply anchoring on
the same quarter a year ago is already a strong prediction.

**Signal model:** We take the FRED retail-sales index, average it over Walmart's
fiscal quarter (Feb–Apr, May–Jul, Aug–Oct, Nov–Jan), then *lag it by one quarter*
before feeding it into a regression. That lag is non-negotiable: it ensures we
are only using data that was published before the quarter we are predicting.

**Evaluation:** We train on a growing historical window and forecast exactly one
quarter ahead, repeating this walk-forward for every quarter from 2014 onward.
We report MAPE (mean absolute percentage error) — the average miss as a fraction
of actual revenue.

---

## Why the Signal Works Pre-COVID

FRED RSXFS is a broad measure of U.S. consumer spending. Walmart, as the
largest U.S. retailer, captures roughly 10–15% of total retail sales. When
consumer spending accelerates in one quarter, Walmart tends to benefit in the
*next* quarter as restocking, promotional cycles, and traffic patterns adjust.
The one-quarter lag relationship is economically sensible: it reflects the
transmission lag from aggregate demand to a single retailer's reported revenue.

---

## Why COVID Broke It — Do Not Fit a Line Through 2020

Three forces decoupled the historical relationship in 2020–2021:

1. **Category mix:** Pandemic buying concentrated in grocery, household staples,
   and pharmacy — Walmart's stronghold — disproportionately more than in the
   broad FRED index (which includes restaurants, auto dealers, gas stations).

2. **Fiscal stimulus distortions:** Three rounds of direct payments (CARES Act,
   December 2020, American Rescue Plan) created demand spikes that have no
   analogue in the regression's training history.

3. **Supply-chain lumpiness:** Inventory shortages in 2021 made revenue timing
   erratic in ways that broke the smooth quarter-to-quarter signal relationship.

Blindly fitting through 2020 would imply the signal explains COVID-era sales —
it does not. The model's COVID MAPE of 4.21% (vs. the naive 2.07%) is evidence
of degradation, not a data anomaly.

---

## What Would Change Our Mind

The "signal does not beat naive on the full sample" verdict is not the final
word. Three things could strengthen the case for the signal:

1. **Post-COVID stabilisation:** We have only 17 quarters of post-COVID data.
   If the relationship re-establishes itself over the next two years, an updated
   analysis would likely tip back in the signal's favour ex-COVID.

2. **Regime-aware modelling:** A two-regime specification (normal vs. shock
   periods) that down-weights or excludes structural breaks would likely show
   the signal is genuinely useful in the non-shock regime.

3. **Enhanced signal construction:** Using FRED sub-categories (e.g.,
   food and beverage stores, general merchandise) that map more closely to
   Walmart's revenue mix could sharpen the signal.

---

## Key Caveats

* Data covers Jan 2010 – Jan 2026 (65 Walmart quarters, 195 FRED months).
* OOS evaluation covers 44 quarters (2014 onward). Short history for structural
  conclusions.
* Only a simple OLS model was tested. Non-linear or ensemble methods may
  perform differently.
* MAPE differences of 0.5–1 pp sound small but correspond to $0.5–1B in
  prediction error at current revenue scale.

---

*Analysis notebook and full methodology in `analysis.ipynb`.*
*Prompt log and orchestration reflection in `prompts.md`.*
