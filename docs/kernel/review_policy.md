<!--
Vendored from agentic-workforce-kernel @ main.
Do not edit — update by re-vendoring from the source repo.
-->

# Review Policy

## Code review

- Every PR requires at least one human approval before merge.
- PRs touching declared "chokepoint" modules require two approvals.
- Automated AI review is advisory only; it does not substitute for human review.
- CodeQL (or equivalent SAST) must be clean — zero high/critical alerts.

## Output review (agent outputs)

- Every Worker output MUST be reviewed by a designated Critic before reaching the HITL gate.
- The Director does not directly approve Worker outputs; the Director only consumes
  Critic-approved artifacts.
- The HITL gate pauses the workflow; the human reviews summarised artifacts before any
  terminal sink (PR, deliverable, or external action) is reached.
- Terminal sinks that emit an external artifact (e.g., a memo, a published model) MUST trigger
  a human notification.

## Evaluation harness

- Project-level KPIs are declared in `docs/projects/<project>/kpis.md`.
- A regression gate in CI blocks merge if the primary KPI regresses by more than the
  project-defined threshold.
- Baselines are committed to `runtime/benchmarks/` and updated only via Critic-approved PR.
