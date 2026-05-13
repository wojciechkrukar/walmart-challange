# Collaboration Rules — walmart-signal-validation

## Branch naming

| Branch type | Pattern | Example |
|------------|---------|---------|
| Feature / task | `task/<short-id>-<slug>` | `task/m3-rolling-cv` |
| Phase work | `phaseN/<slug>` | `phase2/seasonal-naive-baseline` |
| Documentation | `docs/<slug>` | `docs/update-roles` |
| Bugfix | `fix/<slug>` | `fix/add-constant-edge-case` |
| Infra / CI | `infra/<slug>` | `infra/notebook-execution-ci` |

Never push to `main`. All work goes through PRs.

## Parallel work rules

- The Lead Quant and the Critical Reviewer **must never modify the same file in the same PR.** The Critical Reviewer reviews — they do not edit code.
- Phase 1 (data ingestion + baseline) MUST complete before Phase 3 (signal model) starts. This ordering is a guardrail, not a preference.
- The Director never edits `analysis.ipynb` directly — the Director only orchestrates Tasks that result in Lead-Quant edits.

## Who touches what

| Path | Authorised agents |
|------|------------------|
| `analysis.ipynb` | Lead Quant only |
| `data/**` | **No agent.** Read-only source files. |
| `memo.md` | Lead Quant (drafts) → Critical Reviewer (audits causal language) → Director (final formatting) |
| `prompts.md` | Director (orchestration log) |
| `requirements.txt` | Lead Quant |
| `TODO.md` | Director only |
| `docs/kernel/**` | **No agent in this Mission.** Vendored, requires kernel-version bump + HITL approval. |
| `docs/team/**` | Director only (with Critical Reviewer sign-off on `roles.md` and `escalation_matrix.md`) |
| `docs/projects/walmart-signal-validation/**` | Director (orchestration docs), Lead Quant (`architecture.md`, `evaluation-harness.md`), Critical Reviewer (`structural-breaks.md` causal language) |
| `docs/llm-roster.md` | Director only (Class E PR — HITL approval required) |
| `docs/milestones.md` | Director only |
| `docs/delivery_kpis.md` | Director (with Critical Reviewer sign-off) |
| `runtime/agent_handoffs/**` | Director only |
| `runtime/run_reports/**` | Director only |
| `runtime/benchmarks/**` | Lead Quant (writes new baseline) → Critical Reviewer (approves) → Director (commits) |
| `runtime/logs/**` | Any agent (append-only) |
| `runtime/validation/**` | Critical Reviewer |
| `.github/workflows/**` | Director (with HITL approval) |

## Conflict resolution

1. If the Lead Quant and the Critical Reviewer disagree on whether an artifact passes a guardrail, the Critical Reviewer's rejection stands by default.
2. The Lead Quant may request adjudication by the Director. The Director consults the Mission Brief; the Mission Brief's literal text is authoritative.
3. If the Mission Brief is ambiguous, the Director escalates to HITL.
4. The Director's adjudication is logged in `runtime/run_reports/`.

## READ-ONLY zones

- `docs/kernel/**` — vendored from `wojciechkrukar/agentic-workforce-kernel`. All files have provenance notes at the top. Changes require a kernel-version bump in the same PR, subject to HITL approval.
- `data/**` — source CSVs are immutable for the duration of the Mission. The Lead Quant loads them via pandas; no transformation is written back to disk under `data/`.
- `challange_docs/**` — original Mission inputs from HITL. Never modified.
