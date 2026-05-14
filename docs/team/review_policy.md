# Review Policy — YipitData Signal Validation

> Project-specific extension of `docs/kernel/review_policy.md`.

## Artifact class matrix

| Class | Description | Required reviewers | Additional requirements |
|-------|-------------|--------------------|--------------------------|
| **A** | Documentation only (`docs/**`, `README.md`, `TODO.md`, `WALKTHROUGH.md`) | 1 × Director | None |
| **B** | Notebook structural changes (cell reorder, prose, no code-cell mutation) | 1 × Director + 1 × Reviewer | Restart-and-Run-All passes |
| **C** | Notebook code-cell mutation (data load, cleaning, EDA) | 1 × Reviewer | Restart-and-Run-All passes; anti-pattern audit |
| **D** | Modelling code (baseline, OOS CV, signal evaluation) | 1 × Reviewer (STRICT) | Anti-pattern audit + numerical sanity check |
| **E** | Final submission bundle (`analysis.ipynb` + `memo.md` + `prompts.md`) | 1 × Reviewer + 1 × Director + HITL | All Class-D criteria + memo claims trace to notebook results |

## Merge / commit blockers (apply to all classes)

A change MUST NOT be marked DONE if **any** of the following are true:

- [ ] An API call to FRED, yfinance, SEC EDGAR, or any external data source is introduced.
- [ ] A primary data input is read from anywhere other than `data/`.
- [ ] A randomised K-fold or shuffled split appears anywhere in the modelling code.
- [ ] In-sample R² (or in-sample anything) is reported as the success metric for the FRED-vs-baseline comparison.
- [ ] A model is fit through 2020 with no regime indicator and no explicit caveat.
- [ ] The Seasonal Naive Baseline is missing or was added **after** an alternative model.
- [ ] The Walmart revenue used as a predictor for quarter Q was reported on a date later than the FRED snapshot used for the same prediction.
- [ ] `prompts.md` is missing or lacks the < 200-word reflection.
- [ ] `memo.md` exceeds one printed page or omits the "what would change my mind" answer.
- [ ] The notebook does not run end-to-end from a fresh kernel.

## Reviewer checklist (per Review Request)

1. Classify the artifact (A–E).
2. Walk the anti-pattern audit (`docs/kernel/review_policy.md` §6) and write a verdict for **each** item.
3. Verify all merge blockers above are clear.
4. Verify the Task Brief's acceptance criteria.
5. Issue an explicit verdict (APPROVE / REQUEST_CHANGES / REJECT) with named findings.

## Anti-falsification clause

The Reviewer MAY NOT approve any claim of the form "the FRED signal beats the baseline by X" without:
- A stated baseline definition that matches `docs/projects/yipitdata-signal/methodology.md`.
- An OOS error metric (MAPE or RMSE) computed over forward-rolling splits.
- A 95% confidence interval, bootstrap distribution, or comparable uncertainty quantification.
- A subsample analysis that excludes 2020Q1–2021Q1 and reports the same metric.
