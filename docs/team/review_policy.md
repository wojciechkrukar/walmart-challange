# Review Policy — walmart-signal-validation

> Project-specific extension of `docs/kernel/review_policy.md`.

## PR class matrix

| Class | Description | Required reviewers | Additional requirements |
|-------|-------------|-------------------|------------------------|
| **A** | Documentation only (markdown, no code change) | 1 × Director | None |
| **B** | Notebook narrative-only edits (markdown cells) | 1 × Director + 1 × Critical Reviewer | None |
| **C** | Notebook code cells (analysis logic) | 1 × Critical Reviewer (mandatory) + 1 × Director | Notebook executes end-to-end; OOS metrics match baseline.json |
| **D** | Methodology change (CV scheme, lag, baseline formula) | 1 × Critical Reviewer + 1 × Director + HITL approval | Updated `architecture.md` + new `runtime/benchmarks/baseline.json` |
| **E** | LLM tier matrix change OR kernel-doc change | 1 × Director + HITL approval | Provenance bump for kernel docs; rationale in PR description |

## Universal merge blockers (all classes)

A PR MUST NOT be merged if any of the following are true:

- [ ] CI is failing (notebook execution, lint, or CodeQL).
- [ ] `docs/kernel/**` is modified without a provenance-bump commit and HITL approval.
- [ ] `data/*.csv` is modified — source data is immutable.
- [ ] Any `requests`, `urllib`, `pandas_datareader`, or other network-IO library is imported in `analysis.ipynb`.
- [ ] Any `KFold`, `ShuffleSplit`, `train_test_split(..., shuffle=True)`, or random index permutation appears in the CV scheme.
- [ ] An in-sample R², adjusted-R², or AIC is presented as a headline / verdict-driving metric (annotation in a scatter is permitted with explicit "annotation only" label).
- [ ] The Lead Quant fits a model on the full sample including 2020 without a structural-break section.
- [ ] LLM model name is hardcoded outside the (planned) `llm_factory` module.

## Class-specific blockers

- **Class C** — Critical Reviewer must produce a Critic Verdict (per `task_contracts.md`) confirming all six guardrails pass. The verdict MUST cite specific notebook cell numbers.
- **Class D** — `runtime/benchmarks/baseline.json` must be updated in the same PR with the new metrics. The memo must be updated to match.
- **Class E** — `docs/llm-roster.md` change requires written justification for why the new model is at least as strong as the displaced model on the relevant capability (orchestration / coding / adversarial review).

## Critical Reviewer checklist (mandatory for every Class C+ PR)

1. **Look-ahead bias probe.** Confirm that for predicting Q(t), no feature uses any data published after Q(t-1) closes. Cite the lag-construction cell.
2. **Baseline-imperative probe.** Confirm the Seasonal Naive Baseline is constructed and evaluated *before* the signal model is fitted.
3. **In-sample-R² probe.** Search the notebook for `r2_score`, `rsquared`, `R²`, `R^2`. Any occurrence outside an explicit "annotation only" context is a rejection.
4. **CV-scheme probe.** Confirm CV is forward-only with min-train-window ≥ 16 quarters. Reject any `shuffle=True`, `KFold`, `random_state` on splits.
5. **COVID-handling probe.** Confirm sub-period metrics (Pre-COVID, COVID, Post-COVID, Ex-COVID) are reported separately. Confirm the memo addresses the structural break.
6. **Causation probe.** Confirm the memo and notebook do NOT claim FRED *causes* Walmart revenue. Permitted language: "is associated with", "tends to lead", "predicts in the statistical sense".
