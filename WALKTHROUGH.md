# Walmart Signal Validation — Technical Walkthrough

> **Mission demo guide.** Walks through every layer of the system — from Mission-Brief intake to the COVID-aware out-of-sample verdict — explaining *what* each piece does, *why* it was designed that way, and *where* in the repo it lives.

---

## 1. What this Mission solves

A portfolio manager wants to know whether the monthly U.S. retail sales index (FRED ticker **RSXFS**) is a useful predictor of Walmart's quarterly revenue — over and above what a trivial seasonal repeat already provides. The deliverable is a defensible Yes / No answer with quantified confidence, not a model.

The Mission Brief (in `challange_docs/take_home_exam_candidate.md`) sets eight hard guardrails. The system is built so that the only way to violate any of them is to delete a kernel doc — and that requires HITL approval (Class E PR per `docs/team/review_policy.md`).

---

## 2. Why an agentic kernel for a one-shot data-science task?

Two reasons:

1. **Adversarial review is a feature, not a checkpoint.** A Lead Quant Generator and a Critical Reviewer Critic, instantiated as separate roles with *different* LLMs (Opus 4.7 vs. Opus 4.6), reduce the chance of a Generator blind-spot becoming a delivered defect. The kernel's `creator-critic-pairs.md` pattern formalises this.
2. **Guardrails as code, not as memos.** The Mission Brief lists eight invariants. The kernel turns them into a graded system: per-Phase Critic probes (`docs/team/review_policy.md`), a `guardrail_violations` state field (`docs/projects/walmart-signal-validation/architecture.md`), an escalation matrix (`docs/team/escalation_matrix.md`), and a frozen baseline (`runtime/benchmarks/baseline.json`). Each invariant has at least one place where it is mechanically enforced.

The full kernel template (`wojciechkrukar/agentic-workforce-kernel`, used by `wojciechkrukar/lex-triage-agent`) supports up to 11 roles. This Mission activates only 3, per `docs/projects/walmart-signal-validation/agents.md`.

---

## 3. Architecture in one paragraph

The Director receives the Mission Brief, decomposes it into six Phases, and dispatches Tasks to the Lead Quant. The Lead Quant edits `analysis.ipynb`, which loads `data/retail_sales_fred.csv` and `data/walmart_revenue.csv`, aligns FRED to Walmart's fiscal calendar (FY ends January), constructs lag-1 features, builds the Seasonal Naive Baseline FIRST, then fits an OLS signal model, then evaluates both via forward-rolling time-series cross-validation. After every Phase the Critical Reviewer audits for look-ahead bias, in-sample-R² smuggling, and shuffled-CV defects. The Director reports the COVID-aware sub-period verdict to the HITL via the Final-Memo Sign-off template.

The full mermaid DAG and the `MissionState` TypedDict schema live in `docs/projects/walmart-signal-validation/architecture.md`.

---

## 4. The chokepoint: lag-1 alignment

If you only read one cell of the notebook, read the lag-1 construction cell. Walmart's fiscal Q ends in months 4 / 7 / 10 / 1; FRED is monthly. The mapping table in `architecture.md §Fiscal-quarter mapping` shows that the FRED months used as features for predicting Walmart Q(t) are the months that ended one full Walmart quarter before Q(t) starts. **This is the single mechanism that prevents look-ahead bias.**

The Critical Reviewer's first probe in `docs/team/review_policy.md` audits this cell explicitly. Any future change to the lag scheme is a Class D PR (methodology change), requires HITL approval, and forces a regeneration of `runtime/benchmarks/baseline.json`.

> **Caveat — disclosed in the memo.** A 1-quarter calendar lag is conservative. Walmart's 10-Q is typically published ~2-3 weeks after fiscal-quarter close, so an even more conservative scheme would lag by an additional half-quarter. We chose calendar-Q lag for tractability; tightening this further is a future-Mission item.

---

## 5. The Seasonal Naive Baseline — built FIRST

```
Q(t) = Q(t-4) × (1 + μ)
where μ = mean YoY growth on the *training window only*
```

The Mission Brief's "Baseline Imperative" guardrail forbids fitting any signal model before the baseline is built and evaluated. The notebook's section ordering enforces this. The Critic's second probe verifies that μ is recomputed in *each* CV fold and is never the full-sample mean — a subtle leak that is easy to miss.

Frozen baseline metrics live in `runtime/benchmarks/baseline.json`.

---

## 6. The signal model — OLS, lag-1 only

Two features: lagged quarterly FRED YoY growth and lagged Walmart YoY growth (the latter is a momentum control). `statsmodels.api.OLS` with `add_constant`. The `summary().as_text()` is printed for transparency, but every R² is annotated "annotation only" in the cell narrative — the verdict is OOS metrics only.

A future Mission could add Lasso, gradient boosting, or a small neural net, but the Mission Brief explicitly elevates *interpretability + correctness* over fit; OLS is the correct choice for this answer.

---

## 7. Forward-rolling out-of-sample CV

```python
for i in range(min_train, len(df)):
    train = df.iloc[:i]
    test  = df.iloc[i:i+1]
    # fit baseline on train, fit OLS on train, predict on test, accumulate
```

44 folds, `min_train = 16` quarters (4 years — at least one business cycle). The harness is fully deterministic; no `random_state` is set because no randomness is used. See `docs/projects/walmart-signal-validation/evaluation-harness.md` for the full spec including the list of forbidden constructs (`KFold`, `ShuffleSplit`, `train_test_split(..., shuffle=True)`).

---

## 8. The COVID structural-break audit

Guardrail #5 explicitly forbids "blindly fitting a line through 2020". The protocol in `docs/projects/walmart-signal-validation/structural-breaks.md` mandates:

1. A named COVID window: 2020-Q1 → 2021-Q3 (8 folds in the rolling CV).
2. Sub-period MAPE table: Full / Pre-COVID / COVID / Post-COVID / Ex-COVID.
3. A figure (`fig3_covid_break.png`) shading the window.
4. A plain-English driver explanation in the memo.

The reason the Mission's headline is *conditional* — "signal beats baseline ex-COVID; doesn't on the full sample" — is precisely this audit. Without it, the Lead Quant would have reported a single full-sample MAPE and the Mission would have delivered a misleadingly bearish verdict.

---

## 9. The numbers (frozen)

| Window | Baseline MAPE | Signal MAPE | Verdict |
|--------|---------------|-------------|---------|
| Pre-COVID | 2.02% | 1.29% | **Model wins (~36% improvement)** |
| Ex-COVID | 2.42% | 2.11% | **Model wins (~13% improvement)** |
| Full sample | 2.36% | 2.49% | Baseline wins (COVID-driven) |
| COVID window | 2.07% | 4.21% | Baseline wins (signal degrades sharply) |

Source: `runtime/benchmarks/baseline.json`.

---

## 10. How the kernel docs are organised

| Layer | Where | Purpose |
|-------|-------|---------|
| Universal contracts | `docs/kernel/` | Vendored from `agentic-workforce-kernel`; read-only |
| Project-specific extensions | `docs/team/` | Roles, escalation thresholds, review policy, collaboration rules |
| Project specs | `docs/projects/walmart-signal-validation/` | Pipeline architecture, KPIs, harness spec, COVID protocol |
| LLM tier matrix | `docs/llm-roster.md` | Authoritative model-per-role assignment + rationale |
| Milestone tracker | `docs/milestones.md` | M0–M7 status |
| Per-milestone exit criteria | `docs/delivery_kpis.md` | Checklists |
| In-flight status | `runtime/agent_handoffs/current_mission.md` | Director's working state |
| Frozen results | `runtime/benchmarks/baseline.json` | The verdict numbers |
| Mission summary | `runtime/run_reports/` | Per-Mission audit trail |
| Dispatch tracker | `TODO.md` | Tagged `#TODO:` / `#DONE:` items |

---

## 11. What would be different in a "real" production deployment?

This Mission delivers a one-shot answer in a notebook. A productionised version would:

1. Replace `analysis.ipynb` with `apps/walmart-signal/` (a Python package with a CLI), as in `wojciechkrukar/lex-triage-agent`'s `apps/legal-triage/`.
2. Add an `llm_factory.py` whose `ROLE_TIER_MATRIX` is parity-tested against `docs/llm-roster.md`.
3. Wire LangSmith `@traceable` spans to log every LLM call.
4. Add a CI gate that blocks merges if the OOS MAPE in `baseline.json` regresses by more than the threshold in `docs/team/review_policy.md` Class D.
5. Add a Bai-Perron break detector to automate structural-break flagging — the COVID window is currently hand-coded.

These are explicit future-Mission items, not omissions from the present Mission's scope.
