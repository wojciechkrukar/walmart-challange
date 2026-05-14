## Task Brief

**Task ID:** T001
**Mission ID:** YIPIT-SIGNAL-001
**Title:** Data ingestion + sanity EDA
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** 1 (critical)
**Target milestone:** M1
**Depends on:** HITL clearance only
**Status:** PENDING (will dispatch once `HITL_DECISION: approve` appears)

### Objective

Open `analysis.ipynb`. In a labelled section "§ 1 — Data ingestion and sanity EDA", load both
CSVs from `data/`, verify their SHA-256 hashes against `docs/projects/yipitdata-signal/data-contracts.md`,
and print a brief sanity summary so the Reviewer can confirm the canonical inputs are intact.

### Inputs

- `data/retail_sales_fred.csv` (SHA-256 in `data-contracts.md`)
- `data/walmart_revenue.csv`   (SHA-256 in `data-contracts.md`)
- `docs/projects/yipitdata-signal/data-contracts.md`

### Acceptance criteria

- [ ] SHA-256 of both CSVs is computed in-notebook and compared via `assert` (not just printed).
- [ ] For each series: row count, date range, NaN count, dtype.
- [ ] One overlay plot of YoY growth (FRED resampled to quarter, Walmart quarterly) — clean, not polished.
- [ ] All cells run end-to-end from a fresh kernel.
- [ ] In-line comments explain why each step exists (e.g., "we assert hashes to fail loud if data drifts").
- [ ] A "next step" marker is left at the bottom of § 1 pointing at T002.

### Out of scope

- Any modelling.
- Any merge between the two series (T003 owns the merge with the lag rule).
- Any baseline computation (T002 owns the baseline).

### Forbidden

- API calls of any kind.
- Reading data from anywhere outside `data/`.
- Mutating either CSV in place.
- Using `pd.read_csv(..., parse_dates=True)` without explicitly checking the parsed dtype is `datetime64[ns]`.

### Reviewer audit focus

- Hash assertion present and correct.
- No accidental write to `data/`.
- No accidental import of an HTTP / requests / urllib library.
- The overlay plot is not used as a "result" — it is sanity only; explicit caveat in the cell text.
