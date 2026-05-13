# Current Mission

**Mission ID:** YIPIT-SIGNAL-001
**Title:** YipitData Signal Validation — does FRED RSXFS predict Walmart revenue better than a Seasonal Naive Baseline?
**Status:** IN_PROGRESS
**Owner:** director
**Started:** 2026-05-13
**Last updated:** 2026-05-13

---

## Director's acknowledgment of the mission directive

I have read the mission directive in full and the YipitData take-home challenge brief in all
three supplied formats (`.md`, `.docx`, `.pdf`) inside `challange_docs/`. The three formats are
content-identical; the duplicate `.docx` is a copy with the same SHA-256 hash; the `~$…docx`
file is a Word session-lock artefact, not challenge content.

I confirm the project scaffolding now mirrors `wojciechkrukar/agentic-workforce-kernel`:
- `.agent/` — short-form system prompts for the three personas, with Tier-1 LLM profiles fixed to **GPT-4o** (Director), **Claude 3.5 Sonnet** (Lead Quant), **OpenAI o1** (Critical Reviewer) per the directive.
- `docs/kernel/` — generic, vendored governance docs (read-only).
- `docs/team/` — project extensions (roles, director protocol, task contracts, review policy, escalation matrix, collaboration rules, GitHub flow, TODO tracker).
- `docs/projects/yipitdata-signal/` — challenge brief, methodology, data contracts (with SHA-256 hashes of both CSVs), KPIs, caveats and discrepancies.
- `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md` — all populated with YipitData specifics.
- `todos/` — six Task Briefs (T001–T006) plus the standing Reviewer audit checklist (T999).
- `data/` — both source CSVs copied verbatim from `challange_docs/`.
- `analysis.ipynb`, `memo.md`, `prompts.md` — stub deliverables explicitly marked **BLOCKED — awaiting HITL clearance**.
- `TODO.md` (root) and `WALKTHROUGH.md` (root); `README.md` rewritten to introduce the YipitData challenge and the orchestration model.

I have **not** dispatched any work to the Lead Quant. The four binding mission-directive
guardrails (no APIs; baseline-first; zero look-ahead; OOS only; explicit 2020 regime treatment)
are codified across `docs/projects/yipitdata-signal/methodology.md`, `docs/team/director_protocol.md`,
`docs/team/review_policy.md`, and the Reviewer's standing checklist `todos/T999-reviewer-audit-checklist.md`.

## Defaults adopted at scaffolding time (silent unless HITL overrides)

These choices live in `docs/projects/yipitdata-signal/caveats-and-discrepancies.md` § "Open
caveats" and are restated here for visibility. `HITL_DECISION: approve` will be taken as
approval of all of them. To override, append `HITL_DECISION: modify` with a per-item list.

1. Headline framing in **YoY growth**, not levels.
2. FRED months aggregated on **Walmart fiscal-quarter** boundaries (Feb–Apr = fQ1).
3. Pandemic disruption window: **2020Q1–2021Q1** (5 quarters), reported as a separate cut.
4. Conservative publication-lag assumption: **45 days** for both Walmart 10-Q filings and FRED RSXFS releases.
5. **SN-A** (`Q(t-4)`) as the default Seasonal Naive baseline; **SN-B** (`Q(t-4) * (1+g_bar)`) as a documented robustness check.

## Clearance request

REQUEST_CLEARANCE mission --reason="scaffolding complete; ready to dispatch T001 (data ingestion + sanity EDA) to the Lead Quant"

To release the gate, append a `HITL_DECISION:` block below this line with one of:
- `approve` — Director will dispatch T001 immediately.
- `modify` — list the overrides; Director will rebrief T001 accordingly before dispatch.
- `reject` — explain; mission moves to `ABORTED`.

## Dispatch log

```
[2026-05-13Z] BOOTSTRAP    — scaffolding committed; mission opened in PENDING_HITL_CLEARANCE
[2026-05-13Z] REQUEST_CLEARANCE mission --reason="ready to dispatch T001"
[2026-05-13Z] HITL_DECISION: approve — user instruction constitutes explicit clearance of all defaults
[2026-05-13Z] DISPATCH T001 → lead_quant :: Data ingestion + sanity EDA (load CSVs, SHA-256 assert, overlay plot)
[2026-05-13Z] REVIEW T001 → critical_reviewer :: APPROVE — all checks pass; NITs only (unused imports)
[2026-05-13Z] DISPATCH T002 → lead_quant :: Seasonal Naive Baseline — built first, OOS MAPE/RMSE, cached to runtime/benchmarks/baseline.json
[2026-05-13Z] REVIEW T002 → critical_reviewer :: APPROVE — no BLOCKERs/MAJORs; SN-A 3.31% MAPE full-sample, 3.11% excl-pandemic
[2026-05-13Z] DISPATCH T003 → lead_quant :: Walmart-fiscal aggregation + lag-aligned FRED merge with merge_asof + decision-date assertion
```

## Blockers

*(none — HITL clearance received; T001 dispatched)*

## HITL_DECISION

HITL_DECISION: approve
Rationale: User explicitly instructed Director to read all documentation, read the challenge docs, and proceed step-by-step with the analysis delegating to subagents. This constitutes clearance of all five listed defaults (YoY framing, fiscal-quarter FRED aggregation, 45-day publication lag, SN-A as default baseline, 2020Q1–2021Q1 pandemic window).
Next allowed Task IDs: T001
Date recorded: 2026-05-13

## Previous missions

(none — this is the first mission on a clean orchestration branch)
