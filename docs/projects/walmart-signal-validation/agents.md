# Agents — walmart-signal-validation

This Mission instantiates 3 of the 11 kernel roles. The other 8 (Implementer, Reviewer, Triage, Delivery, Vision Specialist, Dataset Curator, Eval Engineer, QA Tester) are not active for this single-notebook Mission and are documented for completeness only in `docs/team/roles.md`.

| Role | Persona name in Mission Brief | LLM (Tier 1) | Active in Phases |
|------|------------------------------|-------------|------------------|
| Director | The Director (Orchestrator) | Claude Opus 4.7 | All |
| Generator (Implementer) | The Lead Quant | Claude Opus 4.7 | P1, P2, P3, P4, P6 |
| Critic | The Critical Reviewer (Adversary) | Claude Opus 4.6 | All |

See `docs/team/roles.md` for the long-form mission, KPIs, escalation triggers, and rationale per agent. See `docs/llm-roster.md` for the authoritative tier matrix and model-selection rationale.

## Why only three agents?

The Mission Brief explicitly names three personas. The kernel template supports more (Vision Specialist, Dataset Curator, etc.) but invoking unused agents would violate the kernel's principle that *every active agent must own a measurable artifact*. The Director, Lead Quant, and Critical Reviewer cover the full surface area:

- The **Director** owns orchestration, guardrails, and HITL communication.
- The **Lead Quant** owns every `analysis.ipynb` cell.
- The **Critical Reviewer** owns every Phase-exit verdict and the `guardrail_violations` field.

If a future iteration adds, say, a backtest with multiple tickers, the kernel's `Eval Engineer` role would be activated and given ownership of `runtime/benchmarks/`.
