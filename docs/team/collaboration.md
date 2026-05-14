# Collaboration Rules — YipitData Signal Validation

## Branch naming

| Branch type        | Pattern                       | Example                                  |
|--------------------|-------------------------------|------------------------------------------|
| Orchestration boot | `copilot/<short-slug>`        | `copilot/initialize-agentic-workflow`    |
| Task               | `task/T<NNN>-<slug>`          | `task/T001-data-ingestion`               |
| Documentation     | `docs/<slug>`                 | `docs/update-roles-table`                |
| Bugfix             | `fix/<slug>`                  | `fix/lag-alignment`                      |
| Infra / CI         | `infra/<slug>`                | `infra/notebook-smoke-test`              |

Never push to `main`. All work goes through PRs.

## Parallel work rules

- The team is **three personas, one mission, one branch at a time**. We do not parallelise modelling work.
- The Lead Quant works on one Task Brief at a time; the next Brief is dispatched only after the
  Reviewer issues APPROVE on the previous one.
- Documentation-only PRs (Class A) MAY proceed in parallel with modelling PRs.
- The Director MUST update `runtime/agent_handoffs/current_mission.md` before and after each
  dispatch so any agent reading the file knows the full in-flight picture.

## Who touches what

| Path                                             | Authorised agents                                      |
|--------------------------------------------------|--------------------------------------------------------|
| `analysis.ipynb`                                 | Lead Quant only (Reviewer reads, never writes)         |
| `memo.md`                                        | Lead Quant (drafts) → Director (final polish)          |
| `prompts.md`                                     | Director (curates the prompt log + reflection note)    |
| `data/**`                                        | **Read-only for all agents**                            |
| `docs/kernel/**`                                 | Director only (provenance bump required)                |
| `docs/team/**`                                   | Director + Reviewer                                     |
| `docs/projects/yipitdata-signal/**`              | Director (architecture) + Lead Quant (methodology)      |
| `docs/llm-roster.md`                             | Director only                                           |
| `runtime/agent_handoffs/**`                      | Director                                                |
| `runtime/run_reports/**`                         | Director                                                |
| `runtime/validation/**`                          | Critical Reviewer                                       |
| `runtime/logs/**`                                | Any agent (append-only)                                 |
| `.agent/**`                                      | Director (with HITL approval for changes after kickoff) |
| `TODO.md`                                        | Director only                                           |
| `todos/**`                                       | Director (Task Briefs)                                  |

## Conflict resolution

1. If the Lead Quant and Reviewer disagree on a methodology choice, the Director arbitrates.
2. If the Director cannot break the tie within one round, escalate to HITL.
3. The more conservative choice (i.e., the one less prone to look-ahead bias) wins by default.

## READ-ONLY zones

- `docs/kernel/**` — vendored from the kernel; provenance note at the top of each file.
- `data/**` — the canonical CSVs. Never overwrite. Derived data goes inline in the notebook.
- `challange_docs/**` — the original challenge brief artifacts (`.md`, `.docx`, `.pdf`) plus the
  source CSVs handed to us. Treat as immutable evidence of the original mission.
