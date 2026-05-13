# Run Report — 2026-05-13 — walmart-signal-validation

**Mission ID:** WAL-2026-05-13
**Objective:** Evaluate whether the FRED RSXFS retail-sales index outperforms a Seasonal Naive Baseline at predicting Walmart quarterly revenue, under the strict guardrails declared in the Mission Brief.
**HITL principal:** repo owner

## Tasks dispatched

| Task ID | Phase | Owner | Verb | Outcome |
|---------|-------|-------|------|---------|
| T-P1-01 | P1 Ingest | Lead Quant | RUN ingestion | DONE |
| T-P1-02 | P1 Ingest | Critical Reviewer | REVIEW ingestion | APPROVED (0.95) |
| T-P2-01 | P2 Baseline | Lead Quant | RUN seasonal_naive_baseline | DONE |
| T-P2-02 | P2 Baseline | Critical Reviewer | REVIEW seasonal_naive_baseline --probe=mu_train_only | APPROVED (0.95) |
| T-P3-01 | P3 Signal | Lead Quant | RUN ols_signal_model | DONE |
| T-P3-02 | P3 Signal | Critical Reviewer | REVIEW ols_signal_model --probe=lag_construction | APPROVED (0.90) |
| T-P4-01 | P4 Rolling CV | Lead Quant | RUN forward_rolling_cv | DONE |
| T-P4-02 | P4 Rolling CV | Critical Reviewer | REVIEW forward_rolling_cv --probe=no_kfold,no_inSample_R2 | APPROVED (0.95) |
| T-P5-01 | P5 COVID audit | Critical Reviewer | RUN structural_break_audit | DONE |
| T-P5-02 | P5 COVID audit | Lead Quant | REVIEW structural_break_audit --counter=true | APPROVED |
| T-P6-01 | P6 Memo | Lead Quant | RUN write_memo | DONE |
| T-P6-02 | P6 Memo | Critical Reviewer | REVIEW write_memo --probe=causal_language | APPROVED (0.95) |

Total: 12 dispatches, 0 failures, 0 escalations.

## Critical-Reviewer verdict summary

All six Phase exit gates approved on the first review cycle. No re-dispatch was required. The Critical Reviewer's adversarial probes covered:

- Lag-1 construction cell: confirmed every feature for predicting Q(t) uses only data ≤ Q(t-1). (P3)
- Mean-YoY construction in Seasonal Naive Baseline: confirmed μ is recomputed per training fold, not on the full sample. (P2)
- CV scheme: confirmed no `KFold`, `ShuffleSplit`, or `train_test_split(..., shuffle=True)` appear in the notebook; min train window = 16 quarters. (P4)
- In-sample R² usage: present in OLS `summary()` print but explicitly labelled "annotation only" in the cell narrative — not used as headline metric. (P3)
- COVID handling: dedicated structural-break section + `fig3_covid_break.png` + sub-period table. (P5)
- Causal-language probe on `memo.md`: zero occurrences of "causes", "drives", "leads to". (P6)

## KPI snapshot (from `runtime/benchmarks/baseline.json`)

| Window | Baseline MAPE | Signal MAPE | Delta | Verdict |
|--------|---------------|-------------|-------|---------|
| Pre-COVID | 2.02% | 1.29% | −36.1% | **Model wins** |
| Ex-COVID | 2.42% | 2.11% | −12.8% | **Model wins** |
| Full sample | 2.36% | 2.49% | +5.5% | Baseline wins (COVID-driven) |
| COVID window | 2.07% | 4.21% | +103.4% | Baseline wins (signal degrades sharply) |

## Guardrail compliance

| # | Guardrail | Status |
|---|-----------|--------|
| G1 | No external APIs | ✅ pass |
| G2 | Baseline first | ✅ pass |
| G3 | Zero look-ahead | ✅ pass |
| G4 | No in-sample R² as headline | ✅ pass |
| G5 | No k-fold / shuffled CV | ✅ pass |
| G6 | COVID explicit | ✅ pass |
| G7 | No causal claims | ✅ pass |
| G8 | Read-only data | ✅ pass |

`guardrail_violations` at Mission close: `[]`

## Escalations

None.

## Headline finding

> "On a strict out-of-sample, lag-aligned forward-rolling cross-validation, the FRED RSXFS index **beats** the Seasonal Naive Baseline on the **Pre-COVID** sample (MAPE 1.29% vs. 2.02%) and on the **Ex-COVID** sample (2.11% vs. 2.42%). On the **full sample** including COVID, the signal **does not beat** the baseline (2.49% vs. 2.36%) because the COVID window dominates the test errors."

## HITL action requested

Final approval per `docs/team/task_contracts.md` Final-Memo Sign-off template. After approval, the Director will mark M7 ✅ Done in `docs/milestones.md`.

## Open items carried forward

None within the scope of this Mission. A future Mission could:
- Extend the lag-1 horizon to honour actual Walmart 10-Q publication dates (currently lag-1 is calendar-quarter-based, which is conservative but may be over-conservative — see `memo.md` caveat).
- Add a Bai-Perron break detector to automate structural-break flagging.
- Repeat the analysis on additional retailers to test signal generalisation.
