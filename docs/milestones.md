# Milestones — YipitData Signal Validation

> Director-maintained mission tracker. Status updated on each milestone exit-criteria pass.

| ID | Name | Status | Description |
|----|------|--------|-------------|
| M0 | Bootstrap & Scaffolding | 🟡 In Review | Kernel-aligned scaffolding; `.agent/` system-prompt cards; YipitData project pack; data files staged in `data/`; mission file in `PENDING_HITL_CLEARANCE`. |
| M1 | HITL Clearance & Data Ingestion (T001) | 🔲 Open | HITL approves dispatch; Lead Quant loads CSVs, verifies hashes, runs sanity EDA; Reviewer audits load + EDA. |
| M2 | Seasonal Naive Baseline (T002) | 🔲 Open | Baseline built BEFORE any alternative model; OOS MAPE / RMSE recorded; Reviewer confirms no leakage. |
| M3 | FRED Lag-Aligned Merge (T003) | 🔲 Open | Walmart-fiscal aggregation; publication-lag rule applied; Reviewer audits decision-date alignment. |
| M4 | OOS Cross-Validation (T004) | 🔲 Open | Forward-rolling CV; FRED-signal model vs. baseline; bootstrap CIs; full-sample and pandemic-excluded cuts. |
| M5 | Structural-Break Analysis (T005) | 🔲 Open | 2020 regime treatment; causal "why"; falsifiable headline claim. |
| M6 | Submission Bundle (T006) | 🔲 Open | `analysis.ipynb` polished; `memo.md` (≤ 1 page); `prompts.md` curated with reflection; Reviewer APPROVE; HITL clearance. |

## Milestone exit criteria

See [`delivery_kpis.md`](delivery_kpis.md) for per-milestone KPI exit criteria.

## M0 detail (in review)

- [x] `.agent/` directory with system prompts for Director / Lead Quant / Critical Reviewer.
- [x] `docs/kernel/` vendored from `agentic-workforce-kernel` (generic, read-only).
- [x] `docs/team/` project extensions (roles, director protocol, task contracts, review policy, escalation matrix, collaboration, github flow, TODO tracker).
- [x] `docs/projects/yipitdata-signal/` project pack (challenge brief, methodology, data contracts, KPIs, caveats).
- [x] `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md` populated for YipitData.
- [x] `todos/` directory with one Task Brief per execution phase.
- [x] Root-level `TODO.md` (`#TODO:` / `#DONE:` format) seeded with the YipitData execution plan.
- [x] Root-level `WALKTHROUGH.md` and YipitData-aware `README.md`.
- [x] Source CSVs copied verbatim from `challange_docs/` into `data/`.
- [x] Stub deliverables (`analysis.ipynb`, `memo.md`, `prompts.md`) clearly marked **BLOCKED — awaiting HITL clearance**.
- [x] `runtime/agent_handoffs/current_mission.md` opened with `STATUS: PENDING_HITL_CLEARANCE` and the Director's clearance request.
- [x] `runtime/{benchmarks,logs,run_reports,validation}/` exist (`.gitkeep`).
- [x] `.gitignore` extended for notebook / Python artefacts.
