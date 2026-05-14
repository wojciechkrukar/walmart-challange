# Task Contracts — YipitData Signal Validation

> Project-specific task and report templates. For the universal Task schema, see `docs/kernel/task_contracts.md`.

## Task Brief template (Director → Lead Quant)

```markdown
## Task Brief

**Task ID:** T<NNN>
**Mission ID:** YIPIT-SIGNAL-001
**Title:** <one-line title>
**Assigned to:** lead_quant
**Reviewer:** critical_reviewer
**Priority:** <1=critical | 2=high | 3=normal>
**Target milestone:** <M0–M5>
**Depends on:** <task IDs or "none">

### Objective
<What must be accomplished. One paragraph. No ambiguity.>

### Inputs
- <file path or data artifact, e.g. `data/retail_sales_fred.csv`>

### Acceptance criteria
- [ ] <specific, verifiable criterion>
- [ ] Code is in a labelled section of `analysis.ipynb`
- [ ] In-line comments explain the statistical reasoning of every non-trivial step
- [ ] Notebook still runs end-to-end from a fresh kernel after the change
- [ ] Reviewer's anti-pattern audit checklist passes for the touched code

### Out of scope
- <explicit exclusions to prevent scope creep>

### Forbidden
- API calls (FRED, yfinance, SEC EDGAR)
- Randomised K-fold or shuffled splits
- In-sample R² as the headline metric
```

## Review Request template (Director → Critical Reviewer)

```markdown
## Review Request

**Task ID:** T<NNN>
**Artifact(s) under review:** <file paths or notebook cells>
**Mode:** STRICT (default) | SCOPED (only changed lines)

### Anti-pattern audit (mandatory checklist)
The Reviewer MUST address each item explicitly in the Review Report.
- [ ] Look-ahead bias / data leakage
- [ ] Train/test contamination
- [ ] Improper time-series cross-validation
- [ ] In-sample metric reporting
- [ ] Baseline omission or post-hoc baseline
- [ ] Structural-break blindness (esp. 2020 COVID period)

### Acceptance criteria from Task Brief
<copy from Task Brief>
```

## Review Report template (Critical Reviewer → Director)

```markdown
## Review Report

**Task ID:** T<NNN>
**Reviewed by:** critical_reviewer
**Date:** YYYY-MM-DD
**Verdict:** APPROVE | REQUEST_CHANGES | REJECT

### Anti-pattern audit (each item MUST be addressed)
1. Look-ahead bias / data leakage — <verdict + evidence>
2. Train/test contamination — <verdict + evidence>
3. Improper time-series cross-validation — <verdict + evidence>
4. In-sample metric reporting — <verdict + evidence>
5. Baseline omission — <verdict + evidence>
6. Structural-break blindness — <verdict + evidence>

### Findings (severity-ranked)
- **BLOCKER:** <description, location, suggested fix>
- **MAJOR:** <…>
- **MINOR:** <…>
- **NIT:** <…>

### Acceptance-criteria checklist (from the Task Brief)
- [ ] <criterion> — pass / fail
- [ ] <criterion> — pass / fail

### Recommendation
- [ ] APPROVE (no BLOCKER and no MAJOR)
- [ ] REQUEST_CHANGES (BLOCKER or MAJOR present; specify follow-up scope)
- [ ] REJECT (artifact must be redone from scratch; explain why)
```

## Task Completion Report template (Lead Quant → Director)

```markdown
## Task Completion Report

**Task ID:** T<NNN>
**Completed by:** lead_quant
**Date:** YYYY-MM-DD

### What was done
<Summary of the analytical work, methodology choices, and where the code lives in `analysis.ipynb`.>

### Files / cells changed
- `analysis.ipynb` § <section> — reason
- (other files if any)

### Self-audit against forbidden list
- [ ] No API calls introduced
- [ ] No randomised K-fold
- [ ] No in-sample R² as headline metric
- [ ] 2020 handled with explicit regime treatment

### Numerical results
<headline numbers — OOS MAPE, RMSE, baseline comparisons — sufficient for the Reviewer>

### Known limitations / follow-up tasks
<gaps, deferred work, items the Reviewer should pay extra attention to>
```
