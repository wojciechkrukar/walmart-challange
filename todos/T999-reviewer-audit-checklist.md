# T999 — Standing Audit Checklist for the Critical Reviewer

> Not a one-shot Task. This is the standing checklist the Critical Reviewer applies to every
> Review Request. Update only with Director approval.

## Anti-pattern audit (six items, mandatory for every review)

For every Lead Quant artifact, address each item explicitly with **evidence** — cell number,
line, value, alternative-interpretation argument. Silence on an item is a defective review.

1. **Look-ahead bias / data leakage.** For every feature value used at decision date `t`,
   confirm its physical release date `<= t`. Spot-check at least three rows by hand.
2. **Train/test contamination.** No observation appears in both fit and OOS evaluation. Check
   the indices.
3. **Improper time-series cross-validation.** Any `KFold`, `ShuffleSplit`, `StratifiedKFold`,
   `train_test_split(..., shuffle=True)`, or unmarked random shuffle is a BLOCKER.
4. **In-sample metric reporting.** In-sample R², accuracy, etc. may not be the headline.
   In-sample numbers may appear only when explicitly labelled "in-sample, not a result."
5. **Baseline omission.** Every "X beats Y" claim must reference a baseline matching the
   definition in `docs/projects/yipitdata-signal/methodology.md` § 4.
6. **Structural-break blindness.** Any model fit through 2020 with no regime indicator and no
   explicit caveat is a BLOCKER.

## Project-specific checks

- **Data-source check.** No `requests`, `urllib`, `httpx`, `yfinance`, `pandas-datareader`,
  `fredapi`, or `sec_edgar_downloader` import appears in the notebook. Primary inputs are
  read from `data/` only.
- **Hash check.** SHA-256 of both CSVs is asserted in § 1 of the notebook against the values
  in `docs/projects/yipitdata-signal/data-contracts.md`.
- **Walmart-fiscal alignment.** FRED months are aggregated to Walmart fiscal quarters
  (Feb–Apr = fQ1), not calendar quarters.
- **Publication-lag rule.** Both Walmart-self-lag and FRED-month-lag features respect the
  decision-date rule in `methodology.md` § 3. Default conservative assumption: filing /
  release date `= reference period end + 45 days`.
- **Pandemic-excluded cut.** Exists. Window is 2020Q1–2021Q1. Reported alongside full-sample.
- **Falsifiability.** The memo's headline names a specific number, a specific window, and a
  specific threshold for what would change the answer.

## Verdict rubric

| Conditions | Verdict |
|---|---|
| All anti-pattern items pass; all project checks pass; no BLOCKER or MAJOR | APPROVE |
| Any BLOCKER OR ≥ 1 MAJOR | REQUEST_CHANGES (state smallest fix scope that flips to APPROVE) |
| Artifact must be redone from scratch (e.g., wrong baseline definition adopted throughout) | REJECT |

## Output format

Use the **Review Report** template in `docs/team/task_contracts.md`. Write the report to
`runtime/validation/T<NNN>-review.md` with the file name matching the Task being reviewed.
