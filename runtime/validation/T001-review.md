# Review Report — T001

**Reviewer role:** Critical Reviewer  
**Artifact:** analysis.ipynb § 1 (cells 1–8, markdown header + 6 code cells + "next step" markdown)  
**Date:** 2026-05-13  
**Verdict:** APPROVE

---

## Anti-pattern audit

> Six items addressed with cell reference, line, and evidence.

**1. Look-ahead bias / data leakage**  
PASS. No modelling occurs in § 1. The two series (`fred_cq_yoy`, `wmt_yoy`) are computed independently from their respective raw dataframes and are never joined or aligned by index. Cell 6 (lines 87–133) explicitly warns that the calendar-quarter FRED aggregation is "for visualization only" and that the merge with lag alignment is deferred to T003. No feature constructed in § 1 could carry a future value forward.

**2. Train/test contamination**  
PASS (N/A). No splitting code is present in any of cells 1–8. Confirmed by full read of the notebook: no `train_test_split`, no boolean mask partitioning observations, no assignment of rows to "train" or "test" sets. Nothing to contaminate.

**3. Improper time-series cross-validation**  
PASS (N/A). No cross-validation code of any kind. Verified: no `KFold`, `ShuffleSplit`, `StratifiedKFold`, `TimeSeriesSplit`, or `sklearn` import appears anywhere in § 1.

**4. In-sample metric reporting**  
PASS (N/A). No model is fit. No R², RMSE, accuracy, or any statistical metric is reported. Cell 5 (lines 61–84) prints descriptive statistics (row count, date range, NaN count, dtype, min/max) which are data-contract checks, not model metrics.

**5. Baseline omission**  
PASS. Cell 8 (markdown, line 196) reads verbatim: *"→ Next: T002 — Seasonal Naive Baseline / The baseline is built before any FRED-augmented model (non-negotiable ordering per methodology.md § 4)."* Baseline is explicitly deferred; no baseline claim is made in § 1.

**6. Structural-break blindness**  
PASS (N/A). No regression fit anywhere in § 1. The COVID disruption window (2020Q1–2021Q1) is shaded in the sanity overlay (cell 7, lines 157–161), with a label `"COVID disruption (2020Q1–2021Q1)"`. The plot comment (cell 7, lines 136–141) notes this shading "flags the regime-treatment requirement (methodology.md § 8)." No model is fit through this break.

---

## Project-specific checks

**Data-source check — YES**  
Cell 2 (lines 6–14) imports: `hashlib`, `json`, `pathlib.Path`, `numpy`, `pandas`, `matplotlib.pyplot`. No `requests`, `urllib`, `httpx`, `yfinance`, `fredapi`, `pandas_datareader`, or `sec_edgar_downloader`. Comment in cell 2 explicitly states: *"every library here is offline (no HTTP, no API calls). requests / urllib / yfinance / fredapi are explicitly banned per methodology.md."*

**Hash check — YES**  
Cell 3 (lines 17–38) asserts both hashes via `assert actual == expected`. Hardcoded values in `EXPECTED_HASHES`:

| File | Hash in notebook | Hash in data-contracts.md | Match |
|---|---|---|---|
| `data/retail_sales_fred.csv` | `332d0d032b5eb1580d0e24fe3b9213749d2cdbc8f5d1b3b3c126d518a38c5aa1` | `332d0d032b5eb1580d0e24fe3b9213749d2cdbc8f5d1b3b3c126d518a38c5aa1` | ✓ |
| `data/walmart_revenue.csv` | `c116c39388b35c482512649bb0a25bd451989d34343432219fb5c83e67979502` | `c116c39388b35c482512649bb0a25bd451989d34343432219fb5c83e67979502` | ✓ |

Both hashes use `assert`, not just `print`. Cell output shows `✓ … hash OK` for both, confirming both asserts passed in the last execution run.

**No write to data/ — YES**  
No `to_csv()`, `to_parquet()`, `df.to_*`, or `open(..., "w")` call targeting `data/` (or any path) in any cell of § 1. All intermediate frames (`fred_cq`, `fred_cq_yoy`, `wmt_yoy`) exist only in memory.

**No `parse_dates=True` — YES**  
Cell 4 (line 46): `fred_raw = pd.read_csv("data/retail_sales_fred.csv")` — no keyword arguments. Cell 4 (line 51): `wmt_raw = pd.read_csv("data/walmart_revenue.csv")` — same. Both date columns are converted via explicit `pd.to_datetime()` on lines 47 and 52.

**dtype assertion — YES**  
Cell 4 (lines 49–50): `assert pd.api.types.is_datetime64_any_dtype(fred_raw["date"])`. Cell 4 (lines 53–54): same assertion for `wmt_raw["date"]`. The comment correctly explains why `is_datetime64_any_dtype()` is used instead of a hard `datetime64[ns]` check (pandas ≥ 2.0 may return `datetime64[us]`).

**Overlay plot labelled as sanity only — YES**  
Cell 7 (line 136): code comment reads *"T001 — sanity overlay plot"*. The figure title (line 161) includes *"(CALENDAR quarter FRED, modelling uses fiscal)"*. An `ax.annotate()` call (lines 167–176) embeds a visible, bbox-framed note directly on the figure: *"NOTE: This is a sanity plot only, not a result. FRED aggregation here is calendar-quarter for visual alignment; T003 applies the correct fiscal-quarter aggregation."*

**Calendar-vs-fiscal distinction — YES**  
Cell 6 (lines 87–103): calendar-quarter aggregation is justified as *"only need rough visual alignment with the Walmart curve."* Lines 96–101 add an explicit `WARNING` comment that this aggregation is *"NEVER used in any model"* and that *"T003 will aggregate FRED on Walmart fiscal-quarter boundaries, which differ by one month — a mistake that has tripped previous candidates (methodology.md § 2)."* The plot annotation repeats this caveat in the rendered figure.

---

## Findings

### BLOCKERs
None.

### MAJORs
None.

### MINORs
None.

### NITs

**NIT-1: Unused `import json` (cell 2, line 7)**  
`json` is imported but never used in § 1. No functional impact; would produce a linter warning (`F401`). Remove or defer to the cell where it is needed.

**NIT-2: Unused `import numpy as np` (cell 2, line 9)**  
`numpy` is imported but not called in any cell of § 1. All numeric operations go through pandas. Same resolution as NIT-1.

---

## Summary

All six anti-pattern audit items pass (the majority are N/A because § 1 is pure data-ingestion with no modelling). All seven project-specific checks pass with direct evidence. The hash assertion is correct and uses the contract-specified digests. No API imports, no writes to `data/`, no `parse_dates=True`, dtype assertions are present, the overlay plot carries an explicit in-figure caveat, and the calendar-vs-fiscal ambiguity is documented in both comments and the plot annotation. The "next step" marker to T002 is present. Two trivial unused-import NITs do not affect correctness. Verdict: **APPROVE**.
