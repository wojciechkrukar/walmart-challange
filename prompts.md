# Prompt Log — YIPIT-SIGNAL-001

## Orchestration overview

Three AI personas divided the work into reviewed sequential tasks. The **Director** (GPT-4o) owned mission governance: it wrote Task Briefs, read Reviewer reports, and decided whether to approve work or require changes before the next task began. The **Lead Quant** (Claude 3.5 Sonnet) owned all Python in `analysis.ipynb` and the data-driven prose. The **Critical Reviewer** (OpenAI o1) audited each notebook section against a six-item anti-pattern checklist (look-ahead bias, train/test contamination, improper CV, in-sample metric reporting, baseline omission, structural-break blindness) plus project-specific acceptance criteria. No task proceeded until APPROVE was issued. One human-in-the-loop clearance gate fired at mission start to confirm methodology defaults and release T001.

## Prompt log (chronological)

### T001 — Data Ingestion

**Director → Lead Quant:** _[paraphrased]_ Read both CSVs from `data/` only. Assert SHA-256 hashes against `docs/projects/yipitdata-signal/data-contracts.md`. Parse dates explicitly — no `parse_dates=True`. Compute year-over-year growth for both series. Produce one sanity overlay plot labelled "not a result." No frequency alignment for modelling — deferred to T003.

**Outcome:** SHA-256 asserts pass on both files. Sanity overlay with COVID window shaded and a visible "not a result" annotation embedded in the figure.

**Reviewer finding:** APPROVE. All six anti-pattern checks pass. Calendar-quarter FRED aggregation explicitly labelled for visualisation only.

---

### T002 — Seasonal Naive Baseline

**Director → Lead Quant:** _[paraphrased]_ Build SN-A (`Q(t-4)`) and SN-B (`Q(t-4) × (1+ḡ)`) with an expanding-window forward-rolling loop, minimum 16-quarter initial train window. Report OOS MAPE and RMSE for both. Pandemic window 2020Q1–2021Q1. Cache to `runtime/benchmarks/baseline.json`. Build the baseline before any FRED model — non-negotiable ordering per methodology.md § 4.

**Outcome:** SN-A OOS MAPE 3.31% full-sample (49 quarters), 3.11% excl-pandemic (44 quarters). Results written to `baseline.json`.

**Reviewer finding:** APPROVE. Look-ahead trace at `t=16` verified by hand; first-fold publication-lag check confirms `Q(t-4)` data was available before the decision date.

---

### T003 — FRED Fiscal Merge with Publication Lag

**Director → Lead Quant:** _[paraphrased]_ Aggregate FRED RSXFS to Walmart fiscal quarters (Feb–Apr = fQ1, May–Jul = fQ2, Aug–Oct = fQ3, Nov–Jan = fQ4). Apply 45-day publication lag per FRED month-end. Join to the Walmart frame using `merge_asof(direction="backward")`. Add a hard `assert` that no row violates the lag constraint. Data preparation only — no modelling.

**Outcome:** 65-row merged frame with `decision_date`, `rsxfs_yoy`, and `revenue_yoy` aligned under the lag constraint. Hard assertion passes on all 65 rows. January-to-`(year-1, Q4)` fiscal edge case verified.

**Reviewer finding:** APPROVE. Publication-lag merge spot-checked for three quarters; fiscal-quarter mapping confirmed for five date examples.

---

### T004 — Out-of-Sample Cross-Validation

**Director → Lead Quant:** _[paraphrased]_ Fit M1 (OLS of `revenue_yoy` on `rsxfs_yoy`) in an expanding-window loop, initial 16-quarter window, step 1. Compute OOS MAPE and RMSE. Compare to SN-A over the matched OOS window. Bootstrap the MAPE delta (10,000 draws) for a 95% CI. Label in-sample R² explicitly as "NOT A RESULT." Cache to `runtime/benchmarks/oos_errors.json`.

**Outcome:** M1 OOS MAPE 2.57% over 42 quarters; matched SN-A 3.64%; delta 1.07 pp; 95% bootstrap CI [+0.41, +1.65 pp]. In-sample R² segregated with explicit disavowal label.

**Reviewer finding:** APPROVE. Forward-rolling assertion (`train_end_idx < test_idx`) confirmed live at execution. Three leakage vectors examined and cleared.

---

### T005 — Structural Break Analysis

**Director → Lead Quant:** _[paraphrased]_ Produce an annotated YoY overlay with pandemic window shaded. Fit M1 on sub-samples (pre-pandemic, pandemic, post-pandemic) to quantify beta collapse. Write a 4-point prose causal explanation. Print a falsifiable claim using only locked OOS figures from `oos_errors.json`.

**First submission — Reviewer finding:** REQUEST_CHANGES (MAJOR). The falsifiable claim in Cell 35 cited **0.74 pp** improvement — the delta computed against SN-A over a misaligned window (SN-A's full 49-quarter OOS vs. M1's 42 quarters). The correct aligned delta is **1.07 pp**, restricting SN-A to the same 42-quarter window as M1.

**Lead Quant fix:** Recomputed SN-A MAPE explicitly over the matched 42-quarter M1 OOS window (3.64%); delta = 3.64% − 2.57% = 1.07 pp. Falsifiable claim rewritten with corrected figure and the excl-pandemic version (1.17 pp, CI [+0.52, +1.74 pp]).

**Second submission — Reviewer finding:** APPROVE. Aligned delta confirmed in Cell 36. Pandemic window consistency verified across four artefacts.

---

### T006 — Memo + Prompts

**Director → Lead Quant:** _[exact text: see Task Brief in todos/T006-memo-and-prompts-log.md]_ Write `memo.md` (≤ 600 words, portfolio-manager audience, four-part question answered, falsifiable headline, explicit caveats in body). Write `prompts.md` (chronological prompt log with reflection < 200 words). Do not modify `analysis.ipynb`.

**Outcome:** `memo.md` written at ~490 words. `prompts.md` written (this document).

**Reviewer finding:** Pending Director clearance.

---

## Reflection (< 200 words)

The three-persona setup caught the most dangerous errors early. The Lead Quant correctly implemented the publication-lag constraint in T003 — `merge_asof(direction="backward")` with a hard assertion is the right pattern — and the forward-rolling CV loop in T004 had zero structural leakage. Bootstrapping rather than a parametric test was the right call given the small sample and non-normal errors.

The notable failure was in T005: the falsifiable claim compared M1's OOS MAPE against SN-A over a different, longer window, overstating improvement by 0.33 pp (0.74 pp reported vs. 1.07 pp correct). The Reviewer caught it by checking window sizes. The root cause was defaulting to the precomputed delta in `oos_errors.json`, which used SN-A's full 49-quarter window — the wrong denominator once M1's OOS window starts 7 quarters later. Aligned comparisons require restricting both series to the intersection window.

At scale the failure mode is context fragility: past a certain number of tasks the Director loses track of which version of a corrected number is canonical. Versioned artefacts in `runtime/benchmarks/` mitigate this, but a longer mission would need a single "locked headline numbers" document that every persona reads before filing prose or reports.
