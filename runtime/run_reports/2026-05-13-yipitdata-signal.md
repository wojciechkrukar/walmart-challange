# Run Report — YIPIT-SIGNAL-001
**Date:** 2026-05-13
**Mission:** YipitData Signal Validation — does FRED RSXFS predict Walmart quarterly revenue better than Seasonal Naive?
**Status:** COMPLETE
**Branch:** `copilot/initialize-agentic-workflow`

---

## Headline result

FRED RSXFS OLS (M1) beats the SN-A seasonal-naive baseline by **+1.07 pp MAPE** over 42 matched out-of-sample quarters (2015 Q3 – 2026 Q1), with a 95% bootstrap confidence interval of **[+0.41 pp, +1.65 pp]** — entirely above zero.

Excluding the 5-quarter pandemic window (2020Q1–2021Q1): **+1.17 pp** improvement, CI **[+0.52 pp, +1.74 pp]**.

---

## Deliverables

| Artifact | Status | Notes |
|---|---|---|
| `analysis.ipynb` | ✅ DONE | 38 cells, §§1–5; SHA-256 assertions, OOS CV, bootstrap CI, regime plot |
| `memo.md` | ✅ DONE | 581 words, 4 customer questions answered |
| `prompts.md` | ✅ DONE | Chronological T001–T006 log + 194-word reflection |
| `runtime/benchmarks/baseline.json` | ✅ DONE | SN-A/SN-B MAPE/RMSE (49 OOS quarters) |
| `runtime/benchmarks/oos_errors.json` | ✅ DONE | M1/M2 OOS errors + aligned delta + bootstrap CI (42 quarters) |
| `runtime/validation/fig_yoy_regime.png` | ✅ DONE | Annotated YoY dual-line plot with pandemic shading |
| `runtime/validation/T001-review.md` through `T006-review.md` | ✅ DONE | All APPROVE (T005 + T006 after fix cycles) |

---

## Commit history

| Commit | Task | Notes |
|---|---|---|
| `6509c6f` | T001 | Data ingestion, SHA-256 assert, sanity plot |
| `24921cd` | T002 | Lead Quant baseline |
| `32095ba` | T002 | Reviewer APPROVE + mission update |
| `172c07b` | T003 | Fiscal FRED merge + anti-lookahead assert |
| `38597f1` | T004 | OOS CV + bootstrap CI |
| `836d5a7` | T004 | Reviewer APPROVE (MINOR) + mission update |
| `48ee5df` | T005 | Structural break + aligned delta fix (MAJOR-1 resolved) |
| `0ab3e54` | T006 | Final deliverables + oos_errors.json delta correction |

---

## Anti-lookahead compliance summary

- **Publication lag:** FRED feature_release_date = last_month_end + 45 days. Validated by hard assert (`feature_release_date <= decision_date`) passing on all 65 merged rows.
- **CV pattern:** Hand-rolled expanding window, `INITIAL_TRAIN=16`, `shuffle=False`. `train_end_idx < test_idx` assertion checked live (Cell 28).
- **Bootstrap:** 2000 resamples of 42 matched OOS pairs only; no train-set rows included.

---

## Review cycle summary

| Task | First verdict | Final verdict | MAJORs resolved |
|---|---|---|---|
| T001 | APPROVE | APPROVE | — |
| T002 | APPROVE | APPROVE | — |
| T003 | APPROVE | APPROVE | — |
| T004 | APPROVE (MINOR) | APPROVE (MINOR deferred) | — |
| T005 | REQUEST_CHANGES | APPROVE | MAJOR-1: stale 0.74pp → 1.07pp |
| T006 | REQUEST_CHANGES | APPROVE | MAJOR-1: oos_errors.json stale delta → corrected |

---

## Key numbers (locked)

| Metric | Value | Source |
|---|---|---|
| M1 OOS MAPE (42 qtrs) | 2.57% | oos_errors.json + Cell 27 |
| SN-A aligned MAPE (42 qtrs) | 3.64% | Cell 36 |
| Aligned delta (full) | +1.07 pp | Cell 36 |
| 95% CI (full) | [+0.41, +1.65 pp] | Cell 30 |
| Aligned delta (excl-pandemic) | +1.17 pp | Cell 36 |
| 95% CI (excl-pandemic) | [+0.52, +1.74 pp] | Cell 30 |
| SN-A full MAPE (49 qtrs) | 3.31% | baseline.json |
| Bootstrap resamples | 2 000 | Cell 30 |
| Random seed | 42 | Cell 30 |
