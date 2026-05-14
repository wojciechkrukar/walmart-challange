# Walkthrough — running the YipitData Signal Validation orchestration

> Operator-facing guide to driving the 3-persona team end-to-end. Pair this with
> [`docs/team/roles.md`](docs/team/roles.md) for the persona-level detail.

---

## 1. What you, the human, do

You are the **HITL** (Human-in-the-Loop). Your loop is short:

1. Read the Director's status post in [`runtime/agent_handoffs/current_mission.md`](runtime/agent_handoffs/current_mission.md).
2. Decide: clearance to proceed, modification, or stop.
3. Append a `HITL_DECISION:` block to that file.
4. Wait for the next Director status post.
5. At mission end, read `analysis.ipynb`, `memo.md`, `prompts.md` and approve the submission.

You **do not** write code. You **do not** talk to the Lead Quant or Reviewer directly. The
Director is your single point of contact.

## 2. What the Director does at session start

1. Loads its system prompt from [`.agent/director.md`](.agent/director.md).
2. Reads `runtime/agent_handoffs/current_mission.md`.
3. Reads `TODO.md` and the open Task Briefs in `todos/`.
4. If the mission is `PENDING_HITL_CLEARANCE`, posts a clearance request and stops.
5. Otherwise, dispatches the highest-priority unblocked Task to its assigned Worker.

## 3. What the Lead Quant does on dispatch

1. Loads its system prompt from [`.agent/lead_quant.md`](.agent/lead_quant.md).
2. Opens the Task Brief named in the dispatch (e.g., `todos/T001-data-ingestion.md`).
3. Reads the relevant section of [`docs/projects/yipitdata-signal/methodology.md`](docs/projects/yipitdata-signal/methodology.md) and treats it as binding.
4. Implements in `analysis.ipynb` under a labelled section matching the Task ID.
5. Files a Task Completion Report (template in [`docs/team/task_contracts.md`](docs/team/task_contracts.md)) addressed to the Director.

## 4. What the Critical Reviewer does on a Review Request

1. Loads its system prompt from [`.agent/critical_reviewer.md`](.agent/critical_reviewer.md).
2. Walks the standing audit checklist in [`todos/T999-reviewer-audit-checklist.md`](todos/T999-reviewer-audit-checklist.md) — every item gets an explicit verdict in writing.
3. Walks the Task Brief's acceptance criteria.
4. Files a Review Report at `runtime/validation/T<NNN>-review.md` and routes the verdict
   (APPROVE / REQUEST_CHANGES / REJECT) to the Director.

## 5. What the Director does on a verdict

- **APPROVE** — mark the Task `DONE` in `TODO.md`, update `current_mission.md`, dispatch the next Task.
- **REQUEST_CHANGES** — re-dispatch to the Lead Quant with the Reviewer's findings attached. Three round-trips on the same Task triggers escalation per [`docs/team/escalation_matrix.md`](docs/team/escalation_matrix.md).
- **REJECT** — cancel the Task, decompose it, re-create it as a new Task Brief.

## 6. The mission shape (M0 → M6)

```
M0  Bootstrap & Scaffolding              ← we are here (in review)
       ↓ HITL clearance
M1  Data ingestion + sanity EDA         (T001)
       ↓
M2  Seasonal Naive Baseline (FIRST)      (T002)
       ↓
M3  Walmart-fiscal aggregation +
     publication-lag-aware FRED merge    (T003)
       ↓
M4  Forward-rolling OOS CV +
     bootstrap CI on delta_MAPE          (T004)
       ↓
M5  2020 regime treatment +
     causal "why" + falsifiable claim    (T005)
       ↓
M6  memo.md + prompts.md +
     final notebook polish               (T006)
       ↓ Reviewer APPROVE + HITL approve
   SUBMISSION
```

## 7. Operating principles (things to remind the team if it drifts)

- **Baseline first, always.** A model that "beats" something nobody named beats nothing.
- **Lag is harder than it looks.** Almost every junior version of this analysis leaks future
  data through `merge` defaults. The Reviewer must spot-check by hand.
- **In-sample is not a result.** If the Lead Quant prints an in-sample R² as a headline, the
  Reviewer rejects.
- **2020 is not noise.** It is structural. Either model it explicitly or split around it. Never
  silently include it in a global fit.
- **One or two clean figures.** The brief explicitly downweights polish. Don't let the team
  produce a gallery.
- **The memo is one page.** Cut for impact, not completeness.

## 8. Tier toggles

`docs/llm-roster.md` defines three tiers. Default in CI is `LLM_TIER=tier3` (deterministic
stubs, no network). For a real run, set `LLM_TIER=tier1` and provide the relevant API keys via
`.env` (gitignored). No model name is hard-coded outside the LLM factory.

## 9. Where to look when something goes wrong

| Symptom | First place to look |
|---|---|
| Lead Quant produced look-ahead | `runtime/validation/T003-review.md` and `methodology.md` § 3 |
| Reviewer keeps asking for the same fix | `current_mission.md` dispatch log; consider escalation |
| Director dispatched without HITL clearance | `current_mission.md` `STATUS:` line — should be `IN_PROGRESS` not `PENDING_HITL_CLEARANCE` |
| Numbers don't match between memo and notebook | `runtime/benchmarks/*.json` is the source of truth; both must cite it |

## 10. Submission package

When the Director marks the mission `DONE`, the deliverables match the YipitData brief's
expected zip layout:

```
firstname_lastname_yipitdata/
├── analysis.ipynb
├── memo.md
├── prompts.md
└── data/
    ├── retail_sales_fred.csv
    └── walmart_revenue.csv
```

The Director writes the matching mission run report to `runtime/run_reports/`.
