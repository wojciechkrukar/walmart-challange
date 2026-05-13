# Phase 2 Plan — Signal Model + OOS Evaluation + Memo

> Owner: Lead Quant. Critic: Critical Reviewer. Director gate: required before HITL hand-off.

## Objective

Fit an OLS signal model with lagged FRED features, evaluate it via the same forward-rolling harness used for the baseline, perform the COVID sub-period audit, and write the executive memo. The memo's headline must match the Ex-COVID and Full-sample verdicts.

## Steps

| Step | Notebook section | Acceptance |
|------|------------------|-----------|
| 2.1 | `## 6. Signal model — OLS` | OLS on `[fred_yoy_lag1, walmart_yoy_lag1]`; `add_constant`; `summary()` printed; in-sample R² annotated as "annotation only" |
| 2.2 | `## 7. Forward-rolling OOS evaluation` | Same harness as baseline; per-fold predictions concatenated to `cv_df` |
| 2.3 | `## 8. Sub-period split` | Pre-COVID, COVID, Post-COVID, Ex-COVID; metrics in a table |
| 2.4 | `## 9. Structural-break commentary` | Per `structural-breaks.md`; figure `fig3_covid_break.png` |
| 2.5 | `## 10. Verdict cell` | Three-line verdict matching `kpis.md` headline pattern |
| 2.6 | `memo.md` | One page; references the verdict; passes causal-language probe |

## Exit criteria (Phase Gate — Critical Reviewer)

- [ ] OLS uses lag-1 features only — confirmed by line-citation
- [ ] CV harness identical to baseline (no per-fold drift)
- [ ] All four sub-period MAPEs reported
- [ ] Verdict cell quotes OOS numbers, not in-sample
- [ ] `fig3_covid_break.png` exists and shades the COVID window
- [ ] `memo.md` passes the six-probe checklist in `docs/team/review_policy.md`
- [ ] No causal verb ("causes", "drives", "leads to") appears in `memo.md`
- [ ] Reproducibility: `jupyter nbconvert --execute --inplace analysis.ipynb` completes successfully and produces byte-identical metrics

## Hand-off

Director presents to HITL via the Final-Memo Sign-off template in `docs/team/task_contracts.md`.
