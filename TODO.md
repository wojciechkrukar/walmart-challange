# TODO Tracker

> Single source of truth for in-flight work. Director updates on dispatch and completion. Tagged-comment grammar mirrors `wojciechkrukar/lex-triage-agent`.

## Open

- `#TODO:` [m7/director] Present `analysis.ipynb` + `memo.md` to HITL via the Final-Memo Sign-off template in `docs/team/task_contracts.md`. After approval, mark M7 ✅ Done in `docs/milestones.md`. (owner: Director, target: M7)

## In Progress

*(empty — all Phase work complete; awaiting HITL final approval)*

## Done

- `#DONE:` [m0/director] Bootstrap — repo cloned; `data/{retail_sales_fred,walmart_revenue}.csv` placed; `requirements.txt` pinned; full `agentic-workforce-kernel` documentation scaffolding vendored under `docs/kernel/`, `docs/team/`, `docs/projects/walmart-signal-validation/`, plus `docs/llm-roster.md`, `docs/milestones.md`, `docs/delivery_kpis.md`, and `runtime/{agent_handoffs,benchmarks,logs,run_reports,validation}/`. (2026-05-13)
- `#DONE:` [m1/lead-quant] Data Ingestion — FRED monthly + Walmart quarterly loaded, fiscal-Q aligned, lag-1 features constructed and audited. Critic verdict APPROVED (0.95). (2026-05-13)
- `#DONE:` [m2/lead-quant] Seasonal Naive Baseline — Q(t) = Q(t-4) × (1 + μ) implemented; μ computed per training fold; metrics frozen in `runtime/benchmarks/baseline.json`. Critic verdict APPROVED (0.95). (2026-05-13)
- `#DONE:` [m3/lead-quant] Signal Model — OLS on `[fred_yoy_lag1, walmart_yoy_lag1]` with `add_constant`; in-sample diagnostics labelled "annotation only". Critic verdict APPROVED (0.90). (2026-05-13)
- `#DONE:` [m4/lead-quant] Out-of-Sample Rolling CV — 44 forward-rolling folds, min train = 16 quarters, no shuffle / no KFold. Critic verdict APPROVED (0.95). (2026-05-13)
- `#DONE:` [m5/critical-reviewer] COVID Structural-Break Audit — window 2020-Q1..2021-Q3 (8 folds); sub-period table + `fig3_covid_break.png` + plain-English driver explanation. Counter-review by Lead Quant APPROVED. (2026-05-13)
- `#DONE:` [m6/lead-quant] Executive Memo — `memo.md` complete; passes the six-probe checklist in `docs/team/review_policy.md`; zero causal verbs. Critic verdict APPROVED (0.95). (2026-05-13)
- `#DONE:` [bootstrap/director] Discrepancy review of challenge inputs — `take_home_exam_candidate.md`, `.docx`, `.docx (1)`, `.pdf` are content-equivalent. No material discrepancies found that affect requirements or evaluation criteria. (2026-05-13)

## Discrepancy log (challenge inputs)

After cross-reading `challange_docs/take_home_exam_candidate.md`, `take_home_exam_candidate.docx`, `take_home_exam_candidate(1).docx`, and `take_home_exam_candidate.pdf`:

- The `.md` and both `.docx` copies contain identical Mission content.
- `take_home_exam_candidate(1).docx` is a duplicate of `take_home_exam_candidate.docx` (same SHA after `unzip -p word/document.xml`).
- The `.pdf` is consistent with a PDF export of the same `.docx`.
- No additions to the execution plan were required as a result of the cross-file review.

## Guardrails snapshot

| Guardrail | Status |
|-----------|--------|
| G1 No external APIs | ✅ |
| G2 Baseline first | ✅ |
| G3 Zero look-ahead | ✅ |
| G4 No in-sample R² as headline | ✅ |
| G5 No k-fold / shuffled CV | ✅ |
| G6 COVID explicit | ✅ |
| G7 No causal claims | ✅ |
| G8 Read-only data | ✅ |

`guardrail_violations` = `[]`

---

*Awaiting HITL clearance before finalising Mission.*
