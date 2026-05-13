# Structural Breaks — walmart-signal-validation

> Mandatory protocol for handling the COVID-19 break. Authored by the Critical Reviewer; signed off by the Director.

## Why this document exists

The Mission Brief's guardrail #5:

> *"The team must explicitly analyze the 'why'. The memo.md and notebook comments must address periods where the relationship breaks down, specifically handling the structural break caused by the 2020 COVID-19 pandemic. Do not blindly fit a line through 2020."*

Without this protocol, any single OLS line through the full sample would silently average a brittle "panic-buying surge" period (Walmart Q1 FY21, ending Apr 2020) with normal periods, and the Lead Quant's reported metrics would be neither honest nor actionable.

## The COVID window

For this Mission, the COVID window is the closed interval:

| Window | Start | End | Justification |
|--------|-------|-----|---------------|
| COVID  | **2020-Q1** (calendar — Walmart fiscal Q1 FY21, ending 2020-04-30) | **2021-Q1** (calendar — Walmart fiscal Q1 FY22, ending 2021-04-30) | Captures the initial panic-buying surge, lockdown trough in non-essentials, and stimulus-driven rebound. After 2021-Q1 the YoY growth re-stabilises within historical bands. |

The window is encoded as a constant in `analysis.ipynb` and referenced in `memo.md`.

## Required actions in the notebook

The Lead Quant MUST include, in `analysis.ipynb`:

1. A markdown cell titled "Structural break — COVID-19" before the verdict cell.
2. A figure (`fig3_covid_break.png`) overlaying actual vs. baseline vs. model predictions for 2018-2022, with the COVID window shaded.
3. Sub-period metrics reported in a table:
   - Full sample MAPE (model vs. baseline)
   - Pre-COVID MAPE (test rows with date < 2020-01-01)
   - COVID MAPE (test rows in COVID window)
   - Post-COVID MAPE (test rows after window)
   - Ex-COVID MAPE (Pre-COVID ∪ Post-COVID — the "honest" verdict)
4. A plain-English explanation of WHY the relationship broke down (channel mix shift to essentials, stimulus, e-commerce share rebalancing).

## Required actions in the memo

The memo MUST contain a paragraph (≤ 80 words) titled "**Structural break: COVID-19**" that states:

- The window used
- The Pre-COVID / Ex-COVID verdict (signal beats baseline)
- The Full-sample verdict (signal does not beat baseline)
- The implication: the FRED signal is a credible predictor under "normal" macro conditions; it should be muted or paused during regime shifts identified by an external break detector.

## Forbidden actions

- Dropping the COVID rows entirely without reporting both windows.
- Adding a 0/1 "covid" dummy variable as a feature without disclosing it in the memo (this would mechanically fix the metric and disguise the break).
- Re-fitting the OLS coefficients on Post-COVID data only and reporting that as the "model" without the Pre-COVID comparison.
- Smoothing the actuals (e.g., 4-quarter rolling mean) before computing MAPE — this is a leak in spirit even if not in code.

## How a future Mission would extend this

A subsequent Mission could add a Bai-Perron or CUSUM break detector, but that is out of scope for the present deliverables. The current protocol is a manually documented, auditable break — the simplest implementation that satisfies guardrail #5.
