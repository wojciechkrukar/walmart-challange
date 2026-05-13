# Project: walmart-signal-validation

> YipitData Signal Validation Mission — evaluate whether the FRED RSXFS retail-sales index outperforms a Seasonal Naive Baseline at predicting Walmart quarterly revenue, under strict no-look-ahead, out-of-sample-only, COVID-aware guardrails.

## Mission Brief

Captured in `challange_docs/take_home_exam_candidate.md` (and the .docx / .pdf siblings, which are content-equivalent).

## Documentation index

| Doc | Purpose |
|-----|---------|
| [architecture.md](architecture.md) | End-to-end pipeline diagram + fiscal-quarter mapping |
| [agents.md](agents.md) | Agent assignments specific to this Mission |
| [creator-critic-pairs.md](creator-critic-pairs.md) | Lead Quant ↔ Critical Reviewer pairing per Phase |
| [kpis.md](kpis.md) | Strict KPI priority order + guardrail invariants |
| [evaluation-harness.md](evaluation-harness.md) | Forward-rolling time-series CV specification |
| [structural-breaks.md](structural-breaks.md) | COVID-19 handling protocol |
| [phase-1-plan.md](phase-1-plan.md) | Data ingestion + Seasonal Naive Baseline |
| [phase-2-plan.md](phase-2-plan.md) | Signal model + OOS evaluation + memo |
| [telemetry.md](telemetry.md) | What we log per agent run |

## Phase summary

| Phase | Owner | Critic | Exit gate |
|-------|-------|--------|-----------|
| P1 — Ingest | Lead Quant | Critical Reviewer | Both CSVs loaded; quarter-end alignment verified |
| P2 — Baseline | Lead Quant | Critical Reviewer | Seasonal Naive baseline frozen in `runtime/benchmarks/baseline.json` |
| P3 — Signal | Lead Quant | Critical Reviewer | OLS on lagged FRED features; in-sample diagnostics labelled "annotation only" |
| P4 — Rolling CV | Lead Quant | Critical Reviewer | Forward-rolling MAPE + RMSE for full / pre-COVID / ex-COVID windows |
| P5 — COVID audit | Critical Reviewer | Lead Quant (counter-review) | Structural-break section in notebook + memo |
| P6 — Memo | Lead Quant | Critical Reviewer | Memo passes causal-language probe |

## Final verdict (frozen)

The FRED RSXFS signal **beats the Seasonal Naive Baseline in the pre-COVID and ex-COVID regimes**, and **does not beat it on the full sample** because the COVID-19 structural break dominates the test errors. See `memo.md` for full numbers.
