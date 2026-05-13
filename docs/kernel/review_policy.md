<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Review Policy

## Output review (agent outputs)

- Every Worker output MUST be reviewed by at least one Critic before it is marked `DONE`.
- Critic and Worker MUST be distinct personas backed by distinct LLM profiles (per `docs/llm-roster.md`).
- The Critic produces a structured **Review Report** with: verdict (APPROVE / REQUEST_CHANGES / REJECT),
  enumerated findings (severity: BLOCKER / MAJOR / MINOR / NIT), and a verifiable acceptance-criteria checklist.
- A `BLOCKER` finding is a merge-stop. The Director MUST route the Task back to the Worker.

## Code review (PRs)

- Every PR requires at least one human approval before merge.
- Automated review tools (CodeQL, code-review bots) are advisory; they do not substitute for human review.
- A PR that touches `docs/kernel/**` requires a human approver and a `chore: vendor kernel @ <sha>` commit.

## Anti-pattern audit (mandatory for any Critic in a quantitative domain)

The Critic MUST explicitly check for, and report on, each of the following before any APPROVE:
1. **Look-ahead bias / data leakage** — every feature value used at time *t* must have been physically available at time *t*.
2. **Train/test contamination** — no observation may appear in both fit and evaluation folds.
3. **Improper cross-validation for time series** — randomised K-fold is forbidden; only forward-rolling splits.
4. **In-sample metric reporting** — in-sample R², accuracy, etc. may not be used as success metrics.
5. **Baseline omission** — any "X is better than Y" claim must reference a stated baseline that Y could plausibly beat.
6. **Structural-break blindness** — regime shifts (recessions, pandemics, policy changes) must be acknowledged, not averaged over.
