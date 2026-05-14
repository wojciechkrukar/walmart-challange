# TODO Tracker — YipitData Signal Validation

> Single source of truth for in-flight work on `YIPIT-SIGNAL-001`. **Director updates on
> dispatch and completion.** Per-Task Briefs live in [`todos/`](todos/).

## Open

*(none — mission COMPLETE)*

## Awaiting HITL

*(none)*

## In Progress

*(none)*

## Done

- `#DONE:` [m1/lead_quant] **T001** Data ingestion + sanity EDA — SHA-256 assertions pass; overlay plot (commit `6509c6f`)
- `#DONE:` [m2/lead_quant] **T002** Seasonal Naive Baseline — SN-A MAPE 3.31% full / 3.11% excl-pandemic; `baseline.json` written (commits `24921cd`, `32095ba`)
- `#DONE:` [m3/lead_quant] **T003** Fiscal FRED merge — 65-row `analysis_df`, lag assertion passes 65/65 rows (commit `172c07b`)
- `#DONE:` [m4/lead_quant] **T004** OOS CV — M1 MAPE 2.57%; aligned delta 1.07pp; CI [+0.41,+1.65pp]; `oos_errors.json` written (commits `38597f1`, `836d5a7`)
- `#DONE:` [m5/lead_quant] **T005** Structural break + falsifiable claim (1.07pp/1.17pp) after fix cycle (commit `48ee5df`)
- `#DONE:` [m6/lead_quant+director] **T006** `memo.md` (581w) + `prompts.md` (194-word reflection) + `oos_errors.json` aligned delta fix (commit `0ab3e54`)
- `#DONE:` [m0/director] **M0 — Bootstrap & Scaffolding** Kernel-aligned scaffolding mirroring `wojciechkrukar/agentic-workforce-kernel`: `.agent/` system prompts for the 3 personas (GPT-4o / Claude 3.5 Sonnet / OpenAI o1), `docs/kernel/` (vendored, generic), `docs/team/` (project extensions), `docs/projects/yipitdata-signal/` (challenge brief, methodology, data contracts, KPIs, caveats), `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md`, `todos/` (T001–T006 + T999), root `TODO.md` + `WALKTHROUGH.md` + YipitData-aware `README.md`, source CSVs copied verbatim into `data/`, stub deliverables (`analysis.ipynb`, `memo.md`, `prompts.md`) marked **BLOCKED — awaiting HITL clearance**, `runtime/agent_handoffs/current_mission.md` opened with `STATUS: PENDING_HITL_CLEARANCE`. (current PR)

## Discrepancies surfaced from `challange_docs/`

(per the user's instruction to flag any inconsistencies between the three challenge-doc formats)

- The three formats — `take_home_exam_candidate.md`, `take_home_exam_candidate.docx`,
  `take_home_exam_candidate.pdf` — are **content-identical**. The two `.docx` files have
  identical SHA-256 hashes (one is a duplicate copy). Only formatting differs across formats.
  See [`docs/projects/yipitdata-signal/caveats-and-discrepancies.md`](docs/projects/yipitdata-signal/caveats-and-discrepancies.md).
- The lockfile `challange_docs/~$ke_home_exam_candidate.docx` is a Word session-lock artefact,
  not challenge content. Optional follow-up: extend `.gitignore`.

## Open caveats / decisions for HITL to confirm

(restated from `docs/projects/yipitdata-signal/caveats-and-discrepancies.md` § "Open caveats")

- YoY-growth framing for the headline (vs. levels). Defaulting to YoY.
- Walmart fiscal-quarter alignment for FRED aggregation (vs. calendar quarter). Defaulting to fiscal.
- Pandemic disruption window definition: `2020Q1–2021Q1` (5 quarters). Defaulting to this.
- Conservative publication-lag assumption: `release_date = reference_period_end + 45 days` for both Walmart 10-Qs and FRED RSXFS releases.
- SN-A (`Q(t-4)`) as the default Seasonal Naive formulation; SN-B (with average growth) as a robustness check.

A `HITL_DECISION` of `approve` is taken to mean approval of these defaults. To override, append
`HITL_DECISION: modify` plus the override list, and the Director will rebrief T001 accordingly.
