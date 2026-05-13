# Milestones

> Skyfall-style milestone tracker. Director updates on each milestone completion.

| ID | Name | Status | Description |
|----|------|--------|-------------|
| M0 | Bootstrap | ✅ Done | Repo cloned; `data/`, `requirements.txt`, kernel docs vendored, governance scaffolded |
| M1 | Data Ingestion | ✅ Done | FRED monthly + Walmart quarterly loaded, fiscal-Q aligned, lag-1 features verified |
| M2 | Seasonal Naive Baseline | ✅ Done | Q(t) = Q(t-4) × (1 + μ) implemented; μ computed per training fold; metrics frozen in `runtime/benchmarks/baseline.json` |
| M3 | Signal Model | ✅ Done | OLS on lagged FRED + Walmart YoY features; `add_constant` applied; in-sample diagnostics labelled "annotation only" |
| M4 | Out-of-Sample Rolling CV | ✅ Done | Forward-rolling MAPE + RMSE for Full / Pre-COVID / COVID / Post-COVID / Ex-COVID windows |
| M5 | COVID Structural-Break Audit | ✅ Done | Dedicated section + `fig3_covid_break.png`; sub-period table in notebook + memo |
| M6 | Executive Memo | ✅ Done | `memo.md` complete; passes the six-probe checklist; zero causal claims |
| M7 | HITL Final Approval | 🔲 Open | Awaiting human sign-off on memo + notebook |

## Milestone exit criteria

See `docs/delivery_kpis.md` for per-milestone exit-criteria checklists.

## Frozen verdict (M4 + M5)

| Window | Baseline MAPE | Signal-Model MAPE | Verdict |
|--------|---------------|-------------------|---------|
| Pre-COVID (test < 2020-Q1) | 2.02% | 1.29% | **Signal beats baseline (~36% improvement)** |
| Ex-COVID (Pre ∪ Post)      | 2.42% | 2.11% | **Signal beats baseline (~13% improvement)** |
| Full sample                | 2.36% | 2.49% | Baseline wins — **driven by COVID window** |

Numbers persisted to `runtime/benchmarks/baseline.json`.
