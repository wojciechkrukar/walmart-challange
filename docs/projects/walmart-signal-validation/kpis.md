# KPIs — walmart-signal-validation

> Strict priority order. A higher-priority KPI may NEVER be regressed for the sake of a lower-priority one.

## Verdict KPIs (in priority order)

| # | KPI | Definition | Direction | Target |
|---|-----|-----------|-----------|--------|
| 1 | **Guardrail compliance** | Number of `guardrail_violations` at Mission close | Minimise | **Must be 0** |
| 2 | **OOS MAPE — Pre-COVID** | Forward-rolling MAPE, signal model vs. baseline, train end < 2020-Q1 | Minimise | Signal beats baseline |
| 3 | **OOS MAPE — Ex-COVID** | Same, with 2020-Q1..2021-Q1 dropped from test | Minimise | Signal beats baseline |
| 4 | **OOS MAPE — Full** | Same, full sample including COVID | Minimise | Reported with COVID caveat |
| 5 | **OOS RMSE** | Same windows, RMSE | Minimise | Sanity check vs. MAPE |
| 6 | **Reproducibility** | Re-running the notebook yields identical OOS metrics | Boolean | True |

## Hard guardrail invariants (binary — pass/fail)

These are **non-negotiable**. Any failure is a Mission halt.

- [ ] **G1 — No external APIs.** No `requests`, `urllib`, `pandas_datareader`, etc.
- [ ] **G2 — Baseline first.** Seasonal Naive baseline is constructed and evaluated before any signal model.
- [ ] **G3 — Zero look-ahead.** Every feature for predicting Q(t) is constructed only from data published ≤ end of Q(t-1).
- [ ] **G4 — No in-sample R² as headline.** In-sample diagnostics may appear in scatterplots labelled "annotation only"; they may NOT drive the verdict.
- [ ] **G5 — No k-fold or shuffled CV.** Forward-rolling time-series CV only.
- [ ] **G6 — COVID explicit.** A dedicated structural-break section appears in both `analysis.ipynb` and `memo.md`.
- [ ] **G7 — No causal claims.** Memo language is "predicts" / "is associated with"; never "causes" / "drives".
- [ ] **G8 — Read-only data.** `data/*.csv` is never modified.

## Telemetry KPIs (logged but not blocking)

| # | KPI | Definition |
|---|-----|-----------|
| T1 | Mission cycle time | HITL request → final memo (wall clock) |
| T2 | Critic rejection rate | Rejections ÷ total reviews |
| T3 | Total LLM spend (USD) | Sum across all agents |
| T4 | Notebook execution time (sec) | `jupyter nbconvert --execute` end-to-end |

## How verdicts are reported

The memo's headline sentence MUST match the Phase-2/3/4 verdict pattern in `architecture.md`:

> "On a strict out-of-sample, lag-aligned forward-rolling cross-validation, the FRED RSXFS index **beats / does not beat** the Seasonal Naive Baseline on the **<window>** sample (MAPE: <model>% vs. <baseline>%)."
