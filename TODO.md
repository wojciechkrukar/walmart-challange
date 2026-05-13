# TODO — YipitData Signal Validation
## Director's Execution Plan

---

## Agentic Team

| Role | Responsibility |
|---|---|
| **Director (Orchestrator)** | Manages team, enforces guardrails, summarises for HITL |
| **Lead Quant (Generator)** | Writes `analysis.ipynb` — ingestion, baseline, model, CV |
| **Critical Reviewer (Adversary)** | Audits for look-ahead bias, data leakage, faulty causal reasoning, COVID structural break |

Human-in-the-Loop (HITL) communicates only with the Director.

---

## Phase 0 — Project Initialisation ✅
- [x] Read challenge brief (`challange_docs/take_home_exam_candidate.md`)
- [x] Verify `.docx` and `.pdf` copies contain identical content (see discrepancy note)
- [x] Set up directory structure from `agentic-workforce-kernel` template
- [x] Copy data files to `data/` directory
- [x] Prototype analysis in throwaway script to validate logic before notebook

## Phase 1 — Data Ingestion & Exploration
- [x] Load `data/retail_sales_fred.csv` (monthly, Jan 2010 – Mar 2026, 195 rows)
- [x] Load `data/walmart_revenue.csv` (quarterly fiscal, Jan 2010 – Jan 2026, 65 rows)
- [x] Understand Walmart fiscal quarter dates (Q4 ends Jan 31, Q1 Apr 30, Q2 Jul 31, Q3 Oct 31)
- [x] Plot both raw series with COVID region highlighted

## Phase 2 — Fiscal-Quarter Alignment & Lag (Critical Reviewer sign-off required)
- [x] Aggregate monthly FRED to Walmart fiscal quarters (3-month mean)
- [x] Apply **1-quarter lag** on the FRED signal → no look-ahead bias
- [x] Verified: predicting Q(t) uses only FRED data from Q(t-1), published ≥ 3 months before Q(t) ends
- [x] **Critical Reviewer checkpoint passed**: lag alignment audited ✓

## Phase 3 — Seasonal Naive Baseline
- [x] Implement: Q̂(t) = Q(t-4) × (1 + ȳ_yoy) where ȳ_yoy is the mean YoY growth in the training window
- [x] Baseline computed *within* the rolling CV loop (no future data leakage)

## Phase 4 — OLS Signal Model
- [x] Feature: `fred_yoy_lag` = YoY % change of lagged quarterly FRED mean
- [x] Target: `wmt_yoy` = YoY % change of Walmart quarterly revenue
- [x] OLS fit on training window only, predict single OOS step

## Phase 5 — Strict Forward-Rolling Cross-Validation
- [x] Minimum 16-quarter (4-year) training window
- [x] Walk forward one quarter at a time, re-fit on full history to that point
- [x] **No k-fold CV, no shuffling, no in-sample R²** — only OOS MAPE and RMSE
- [x] **Critical Reviewer checkpoint passed**: CV scheme audited ✓

## Phase 6 — COVID Structural-Break Analysis
- [x] Define COVID window: 2020-Q1 (Jan 31, 2020) through 2021-Q3 (Oct 31, 2021) — 8 quarters
- [x] Compute OOS metrics separately: pre-COVID / COVID / post-COVID / ex-COVID
- [x] Visualise residuals by sub-period
- [x] **Critical Reviewer checkpoint passed**: COVID handling audited ✓

## Phase 7 — Deliverables
- [x] `analysis.ipynb` — end-to-end notebook, runs without errors
- [x] `memo.md` — one-page executive memo for a portfolio manager
- [x] `prompts.md` — orchestration prompt log + reflection

---

## Discrepancies Between Challenge Doc Files

After reviewing `take_home_exam_candidate.md`, `take_home_exam_candidate.docx`, and
`take_home_exam_candidate(1).docx`:

- The `.md` file and both `.docx` copies appear to contain **identical challenge content**.
  No material discrepancies were found that affect requirements or evaluation criteria.
- `take_home_exam_candidate(1).docx` is a duplicate of `take_home_exam_candidate.docx`
  (likely created by a save-as or download operation).
- The `.pdf` is assumed to match the `.docx` content (consistent with a PDF export of the same doc).
- **No additions to the execution plan are required** as a result of the cross-file review.

---

## Guardrails Checklist (Director enforces)

| Guardrail | Status |
|---|---|
| No external APIs — only `data/` files | ✅ |
| Seasonal Naive Baseline built before any model | ✅ |
| 1-quarter lag enforced on all FRED features | ✅ |
| Zero look-ahead bias in training/test splits | ✅ |
| Only OOS metrics (MAPE, RMSE) — no in-sample R² headline | ✅ |
| Strict forward-rolling CV (no k-fold) | ✅ |
| COVID structural break explicitly analysed | ✅ |
| Causal reasoning documented in notebook | ✅ |

---

*Awaiting HITL clearance before finalising artifacts.*
