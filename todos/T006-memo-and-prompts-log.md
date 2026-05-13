## Task Brief

**Task ID:** T006
**Mission ID:** YIPIT-SIGNAL-001
**Title:** `memo.md` + `prompts.md` finalisation
**Assigned to:** lead_quant (drafts) + director (polish & curation)
**Reviewer:** critical_reviewer + director
**Priority:** 1 (critical)
**Target milestone:** M6
**Depends on:** T005
**Status:** PENDING

### Objective

Convert the analytical work into the two narrative deliverables required by the YipitData
brief: a one-page executive memo (`memo.md`) and a curated prompt log (`prompts.md`) with a
short reflection on the orchestration's performance. Polish `analysis.ipynb` for fresh-kernel
reproducibility. This is the bundle that goes to the human for final clearance.

### Inputs

- `analysis.ipynb` (final state after T005)
- `runtime/benchmarks/baseline.json`, `runtime/benchmarks/oos_errors.json`
- `runtime/validation/T*-review.md` (Reviewer Reports across the mission)
- `runtime/agent_handoffs/current_mission.md` (the orchestration log)

### Acceptance criteria — `analysis.ipynb`

- [ ] Restart-and-Run-All passes from a clean kernel without errors or warnings (other than
      benign Pandas/NumPy ones, called out in a note cell).
- [ ] Section headers map 1:1 to T001 → T005.
- [ ] One or two clean figures total (per the brief's "clean is enough" guidance).

### Acceptance criteria — `memo.md`

- [ ] ≤ 1 printed page (call it ~600 words as a guide; cut for impact).
- [ ] Audience: a portfolio manager who took stats in college.
- [ ] Answers all four parts of the customer question: yes/no? by how much? what to worry about? what would change our minds?
- [ ] Headline number is falsifiable (per `docs/projects/yipitdata-signal/kpis.md`).
- [ ] At least one explicit caveat (look-ahead, regime, fiscal-calendar, low base rate, …).
- [ ] No prose hides behind footnotes — all caveats are in the body.

### Acceptance criteria — `prompts.md`

- [ ] Chronological log of the orchestration prompts that drove the work (Director → Quant,
      Director → Reviewer, the HITL clearance prompt). Mark exact text where preserved; mark
      summaries where text was paraphrased.
- [ ] One short reflection (< 200 words) on:
      - What the assistants got right.
      - One or two places the Lead Quant got something subtly wrong and the Reviewer caught it.
      - What the orchestration's failure mode would be if scaled (longer context, more tasks).

### Out of scope

- Adding new modelling.
- Re-running the OOS evaluation (results are locked at T004 / T005 unless a Reviewer BLOCKER mandates rework).

### Forbidden

- Memo claims that do not trace to a specific notebook cell or `runtime/benchmarks/` artefact.
- Polishing figures past "clean" — the brief explicitly downweights polish.
- Editing the prompt log to make the orchestration look better than it was.

### Reviewer audit focus

- Every numerical claim in the memo can be cited to a notebook cell or a `runtime/benchmarks/` JSON file.
- The "what would change our minds" sentence is concrete (a metric, a window, a threshold).
- The reflection in `prompts.md` is honest — at least one acknowledged miss.
