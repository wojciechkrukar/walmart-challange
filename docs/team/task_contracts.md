# Task Contracts — walmart-signal-validation

> Project-specific task templates. For the universal task schema, see `docs/kernel/task_contracts.md`.

## Task Brief template (Director → Worker)

```
## Task Brief

**Task ID:** <UUID>
**Mission ID:** WAL-2026-05-13
**Title:** <one-line title>
**Assigned to:** <Lead Quant | Critical Reviewer>
**Priority:** <1=critical | 2=high | 3=normal>
**Phase:** <P1-ingest | P2-baseline | P3-signal | P4-rollingCV | P5-COVID | P6-memo>
**Target milestone:** <M1–M6>
**Depends on:** <task IDs or "none">

### Objective
<What must be accomplished. One paragraph. No ambiguity.>

### Inputs
- <file path or shared-state field>

### Acceptance criteria
- [ ] <specific, verifiable criterion>
- [ ] Notebook cell executes without errors
- [ ] Every code cell has a statistical-reasoning comment
- [ ] Critical Reviewer guardrail checklist passes (see `kpis.md`)

### Out of scope
- <explicit exclusions to prevent scope creep>

### Guardrail reminders (echoed from Mission Brief)
- No external APIs
- Baseline before signal model
- 1-quarter lag enforced
- Forward-rolling CV only — no k-fold, no in-sample R²
- COVID explicitly addressed
```

## Implementation Completion Report (ICR) — Lead Quant → Director

```
## Implementation Completion Report

**Task ID:** <UUID>
**Completed by:** Lead Quant
**Date:** <YYYY-MM-DD>

### What was done
<Summary of changes made.>

### Notebook cells touched
- Cell <N>: <reason>

### Statistical reasoning summary
<One paragraph explaining WHY the chosen approach is correct under the guardrails.>

### Reproducibility check
- [ ] `jupyter nbconvert --execute --inplace analysis.ipynb` exits 0
- [ ] OOS metrics in the notebook match `runtime/benchmarks/baseline.json`

### Known limitations / follow-up tasks
<Any known gaps or deferred work.>

### Self-audit against guardrails
- [ ] No external APIs introduced
- [ ] Baseline built before any signal model
- [ ] All FRED features lagged ≥ 1 quarter
- [ ] No KFold / ShuffleSplit / random_state on CV splits
- [ ] In-sample R² either absent or labelled "annotation only"
- [ ] COVID window explicitly handled (not smoothed over)
```

## Critic Verdict — Critical Reviewer → Director

```
## Critic Verdict

**Task ID:** <UUID>
**Reviewed by:** Critical Reviewer
**Date:** <YYYY-MM-DD>
**Artifact:** <notebook path + cell range, or memo section>

### Adversarial probes attempted
1. <probe 1 — e.g., "Searched for any feature constructed from the test row">
2. <probe 2 — e.g., "Verified mean YoY in baseline is computed on `train` slice only">
3. <probe 3 — e.g., "Confirmed `add_constant` does not silently drop the intercept">

### Findings
- <finding 1 — pass / fail with line/cell reference>

### Verdict
- [ ] **APPROVED** — Lead Quant artifact may proceed to next Phase
- [ ] **REJECTED** — Lead Quant must redo with rationale below
- [ ] **ESCALATED** — Conflict cannot be resolved at Critic level

### Rejection rationale (if applicable)
<Specific defect, with file/line citation.>

### Confidence
<float 0–1>
```

## Final-Memo Sign-off — Director → HITL

```
## Final-Memo Sign-off Request

**Mission:** WAL-2026-05-13 — YipitData Signal Validation
**Date:** <YYYY-MM-DD>

### Deliverables ready for HITL review
- `analysis.ipynb` — executes clean, OOS metrics validated
- `memo.md` — one-page executive summary
- `prompts.md` — orchestration log
- `runtime/benchmarks/baseline.json` — frozen metrics

### Critical Reviewer sign-off
All six Phase gates (M1–M6) approved. Verdicts in `runtime/run_reports/YYYY-MM-DD-walmart-signal-validation.md`.

### Guardrail compliance
- [x] No external APIs
- [x] Baseline before signal model
- [x] 1-quarter lag verified
- [x] Forward-rolling CV only
- [x] COVID explicitly handled

### Headline finding
<One sentence — the verdict.>

### HITL decision required
- [ ] Approve and finalise
- [ ] Request changes (specify)
- [ ] Abort
```
