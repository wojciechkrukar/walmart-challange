## Task Brief

**Task ID:** T005
**Mission ID:** YIPIT-SIGNAL-001
**Title:** 2020 regime treatment + causal "why"
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** 2 (high)
**Target milestone:** M5
**Depends on:** T004
**Status:** PENDING

### Objective

In `analysis.ipynb` § 5, explicitly characterise the 2020 COVID disruption and explain why the
FRED–Walmart relationship would or would not be expected to hold across regimes. Land on a
falsifiable headline claim suitable for the memo.

### Inputs

- The OOS results from T004 (`runtime/benchmarks/oos_errors.json`)
- `docs/projects/yipitdata-signal/methodology.md` § 8–10
- `docs/projects/yipitdata-signal/kpis.md` § "Falsifiability requirement"

### Acceptance criteria

- [ ] One annotated YoY plot of both series with the 2020Q1–2021Q1 disruption window shaded.
- [ ] Either: a regression refit with an `is_pandemic_quarter` regime dummy AND its coefficient
      (with CI) reported; OR a sub-sample fit excluding the regime, reported alongside the
      full-sample fit. State which approach was chosen and why.
- [ ] A short prose block (3–6 sentences) on the causal "why":
      - What is the plausible mechanism by which retail-sector retail sales would lead Walmart revenue?
      - What common factor (consumer-spending demand) might drive both, making the link spurious in some regimes?
      - Why might that mechanism break in a stimulus-driven, supply-constrained regime like 2020–2021?
- [ ] A single, falsifiable headline claim drafted for the memo (one sentence).
- [ ] The Reviewer's anti-pattern audit is filed in `runtime/validation/T005-review.md`.

### Out of scope

- Memo polishing (T006).
- Adding more models. We have enough.

### Forbidden

- Silent "the relationship still holds" claims without a regime check.
- Cherry-picked sub-windows chosen because they make the headline look better.
- Removing the pandemic period without saying so in the memo.

### Reviewer audit focus

- The shaded window in the plot matches the window dropped in the pandemic-excluded cut.
- The regime dummy / sub-sample choice is consistent with what T004 reported.
- The falsifiable claim names a specific number (pp of MAPE) and a specific window.
- The "why" block does not assert causation it has not earned. "Plausibly drives" / "is correlated with" / "is a noisy proxy for" are acceptable; "causes" is not.
